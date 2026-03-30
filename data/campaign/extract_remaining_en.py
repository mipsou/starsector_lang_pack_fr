#!/usr/bin/env python3
"""Extract remaining EN dialogue entries from rules.csv into batch JSON files.
Compares mod rules.csv with vanilla to find untranslated lines."""
import csv
import json
import re
import os

BATCH_SIZE = 10
MOD_CSV = os.path.join(os.path.dirname(__file__), "rules.csv")
VANILLA_CSV = r"D:\Fractal Softworks\Starsector\starsector-core\data\campaign\rules.csv"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "rules_en_batches")

os.makedirs(OUTPUT_DIR, exist_ok=True)

FR_PATTERN = re.compile(r'[éèêëàâäùûüôöïîçÉÈÊÀÂÙÛÔÇ«»]')

# Read vanilla for comparison
vanilla_rows = []
with open(VANILLA_CSV, 'r', encoding='cp1252') as f:
    reader = csv.reader(f)
    for row in reader:
        vanilla_rows.append(row)

# Read mod
mod_rows = []
with open(MOD_CSV, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        mod_rows.append(row)

print(f"Vanilla: {len(vanilla_rows)} CSV rows")
print(f"Mod:     {len(mod_rows)} CSV rows")

entries = []
for i, mod_row in enumerate(mod_rows):
    if len(mod_row) < 5:
        continue

    rule_id = mod_row[0]

    # Skip comments and empty IDs
    if not rule_id or rule_id.startswith('#'):
        continue

    text_col = mod_row[4] if len(mod_row) > 4 else ""
    opts_col = mod_row[5] if len(mod_row) > 5 else ""

    # Check text column - is it EN?
    if text_col and not FR_PATTERN.search(text_col) and len(text_col) > 20:
        # Verify it looks like English prose (not just commands/variables)
        if re.search(r'[A-Z][a-z]+ [a-z]+ [a-z]+', text_col):
            entries.append({
                "csv_row": i,
                "id": rule_id,
                "column": "text",
                "original": text_col,
                "translated": ""
            })

    # Check options column - extract EN text after ':'
    if opts_col and not FR_PATTERN.search(opts_col) and ':' in opts_col:
        # Options format: id:"Text" or id:Text
        option_parts = opts_col.split('\n')
        for part in option_parts:
            if ':' in part and not FR_PATTERN.search(part):
                opt_text = part.split(':', 1)[1].strip().strip('"')
                if len(opt_text) > 10 and re.search(r'[A-Z][a-z]+ [a-z]+', opt_text):
                    entries.append({
                        "csv_row": i,
                        "id": rule_id,
                        "column": "options",
                        "option_line": part,
                        "original": opt_text,
                        "translated": ""
                    })

print(f"Found {len(entries)} EN entries to translate")

# Write batches
batch_num = 0
for i in range(0, len(entries), BATCH_SIZE):
    batch_num += 1
    batch = entries[i:i+BATCH_SIZE]
    outfile = os.path.join(OUTPUT_DIR, f"rules_batch_{batch_num:03d}.json")
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    print(f"  {outfile}: {len(batch)} entries")

print(f"Total: {batch_num} batch files")

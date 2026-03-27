#!/usr/bin/env python3
"""Extract EN GALLERY entries from descriptions.csv into batch JSON files."""
import csv
import json
import re
import os

BATCH_SIZE = 10
INPUT = os.path.join(os.path.dirname(__file__), "descriptions.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "gallery_batches")

os.makedirs(OUTPUT_DIR, exist_ok=True)

FR_PATTERN = re.compile(r'[éèêëàâäùûüôöïîçÉÈÊÀÂÙÛÔÇ«»]')

entries = []
with open(INPUT, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row_idx, row in enumerate(reader):
        if len(row) < 4:
            continue
        if row[1] != "GALLERY":
            continue
        # Check if description (col 3) is still EN (no French accents)
        desc = row[3] if len(row) > 3 else ""
        if not desc:
            continue
        if FR_PATTERN.search(desc):
            continue  # Already translated

        entry = {
            "csv_row": row_idx,
            "id": row[0],
            "title": row[2],
            "original_text": desc,
            "translated_title": "",
            "translated_text": ""
        }
        # Also include text2 (col 4) if present
        if len(row) > 4 and row[4]:
            entry["text2"] = row[4]
        entries.append(entry)

print(f"Found {len(entries)} EN GALLERY entries")

# Write batches
batch_num = 0
for i in range(0, len(entries), BATCH_SIZE):
    batch_num += 1
    batch = entries[i:i+BATCH_SIZE]
    outfile = os.path.join(OUTPUT_DIR, f"gallery_batch_{batch_num:02d}.json")
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    print(f"  {outfile}: {len(batch)} entries")

print(f"Total: {batch_num} batch files")

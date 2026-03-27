#!/usr/bin/env python3
"""Reassemble translated rules.csv entries from batch JSON files.

Reads translated batches from rules_en_batches/ and applies them
back to rules.csv, replacing only the translated columns.
"""
import csv
import json
import os
import glob

BATCH_DIR = os.path.join(os.path.dirname(__file__), "rules_en_batches")
CSV_FILE = os.path.join(os.path.dirname(__file__), "rules.csv")

# Load all translated batches
translations = {}
for bf in sorted(glob.glob(os.path.join(BATCH_DIR, "rules_batch_*.json"))):
    with open(bf, 'r', encoding='utf-8') as f:
        for entry in json.load(f):
            if entry.get("translated"):
                key = (entry["csv_row"], entry["column"])
                translations[key] = entry

print(f"Loaded {len(translations)} translated entries")

if not translations:
    print("No translations found. Make sure batch files have 'translated' field filled.")
    exit(0)

# Read CSV
with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Read {len(rows)} CSV rows")

# Apply translations
applied_text = 0
applied_opts = 0
errors = 0

for (row_idx, column), entry in translations.items():
    if row_idx >= len(rows):
        print(f"  WARNING: row {row_idx} out of range")
        errors += 1
        continue

    row = rows[row_idx]

    # Verify ID matches
    if row[0] != entry["id"]:
        print(f"  WARNING: ID mismatch at row {row_idx}: expected '{entry['id']}', got '{row[0]}'")
        errors += 1
        continue

    if column == "text" and len(row) > 4:
        row[4] = entry["translated"]
        applied_text += 1
    elif column == "options" and len(row) > 5:
        # Options: replace the specific option line
        if "option_line" in entry:
            old_line = entry["option_line"]
            # The option format is id:"text" or id:text
            # We need to replace only the text part after ':'
            colon_idx = old_line.index(':')
            opt_id = old_line[:colon_idx]
            new_line = f'{opt_id}:{entry["translated"]}'

            if old_line in row[5]:
                row[5] = row[5].replace(old_line, new_line)
                applied_opts += 1
            else:
                print(f"  WARNING: option line not found in row {row_idx}: {old_line[:50]}...")
                errors += 1
        else:
            applied_opts += 1

print(f"\nApplied: {applied_text} text + {applied_opts} options = {applied_text + applied_opts} total")
print(f"Errors: {errors}")

# Write CSV back
with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)

print(f"Written {CSV_FILE}")

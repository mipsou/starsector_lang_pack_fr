#!/usr/bin/env python3
"""Reassemble translated GALLERY entries back into descriptions.csv."""
import csv
import json
import os
import glob
import io

BATCH_DIR = os.path.join(os.path.dirname(__file__), "gallery_batches")
CSV_FILE = os.path.join(os.path.dirname(__file__), "descriptions.csv")

# Load all translated batches
translations = {}
for bf in sorted(glob.glob(os.path.join(BATCH_DIR, "gallery_batch_*.json"))):
    with open(bf, 'r', encoding='utf-8') as f:
        for entry in json.load(f):
            if entry.get("translated_text"):
                translations[entry["csv_row"]] = entry

print(f"Loaded {len(translations)} translated GALLERY entries")

# Read CSV
with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Read {len(rows)} CSV rows")

# Apply translations
applied = 0
for row_idx, entry in translations.items():
    if row_idx >= len(rows):
        print(f"  WARNING: row {row_idx} out of range (max {len(rows)-1})")
        continue

    row = rows[row_idx]
    if len(row) < 4:
        print(f"  WARNING: row {row_idx} too short ({len(row)} cols)")
        continue

    # Verify ID matches
    if row[0] != entry["id"]:
        print(f"  WARNING: ID mismatch at row {row_idx}: expected '{entry['id']}', got '{row[0]}'")
        continue

    # Replace title (col 2) and description (col 3)
    if entry.get("translated_title"):
        row[2] = entry["translated_title"]
    row[3] = entry["translated_text"]
    applied += 1

print(f"Applied {applied} translations")

# Write CSV back
with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)

print(f"Written {CSV_FILE}")

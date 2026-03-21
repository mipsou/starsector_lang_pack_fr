"""
Assemble French translations from tr_*.json files into rules.csv.

Each tr_X_Y.json contains [[row_index, "french_text"], ...] where row_index
is the 0-based row number from csv.reader, and french_text replaces column 4 (text).
"""

import csv
import json
import glob
import os
import io

WORKDIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(WORKDIR, "rules.csv")

# 1. Read all CSV rows
with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
    raw = f.read()

# Detect line ending style
if "\r\n" in raw:
    line_ending = "\r\n"
elif "\r" in raw:
    line_ending = "\r"
else:
    line_ending = "\n"
print(f"Detected line ending: {repr(line_ending)}")

reader = csv.reader(io.StringIO(raw))
rows = list(reader)
print(f"Total CSV rows: {len(rows)}")

# 2. Load all tr_*.json files
tr_files = sorted(glob.glob(os.path.join(WORKDIR, "tr_*.json")))
print(f"Found {len(tr_files)} translation files")

total_replacements = 0
errors = []

for tr_file in tr_files:
    with open(tr_file, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for row_idx, french_text in entries:
        if row_idx < 0 or row_idx >= len(rows):
            errors.append(f"{os.path.basename(tr_file)}: row {row_idx} out of range (max {len(rows)-1})")
            continue

        if len(rows[row_idx]) <= 4:
            errors.append(f"{os.path.basename(tr_file)}: row {row_idx} has only {len(rows[row_idx])} columns")
            continue

        rows[row_idx][4] = french_text
        total_replacements += 1

print(f"Total replacements: {total_replacements}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors[:20]:
        print(f"  {e}")

# 3. Write back to CSV
output = io.StringIO()
writer = csv.writer(output, lineterminator="\n")
writer.writerows(rows)
csv_text = output.getvalue()

# Restore original line endings if needed
if line_ending != "\n":
    csv_text = csv_text.replace("\n", line_ending)

with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(csv_text)

# 4. Verify
with open(CSV_PATH, "r", encoding="utf-8") as f:
    verify_raw = f.read()
file_lines = verify_raw.count("\n") + (1 if not verify_raw.endswith("\n") else 0)

verify_reader = csv.reader(io.StringIO(verify_raw))
verify_rows = list(verify_reader)

print(f"\nVerification:")
print(f"  File lines: {file_lines}")
print(f"  CSV rows: {len(verify_rows)}")
print(f"  File size: {os.path.getsize(CSV_PATH):,} bytes")

# Spot check a few translations
print(f"\nSpot checks:")
print(f"  Row 5 text[:60]: {repr(verify_rows[5][4][:60])}")
print(f"  Row 13 text[:60]: {repr(verify_rows[13][4][:60])}")

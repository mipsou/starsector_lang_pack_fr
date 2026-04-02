#!/usr/bin/env python3
"""
extract_full.py — Étape 1 du pipeline de traduction
Extrait les textes EN depuis le CSV vanilla (rules.csv)
Produit texts_batch_1.json ... texts_batch_N.json (batches de ~50 textes)
"""

import csv, json, os, math

BASE = os.path.dirname(os.path.abspath(__file__))
VANILLA_CSV = os.path.join(
    os.environ.get("STARSECTOR_CORE", r"D:\Fractal Softworks\Starsector\starsector-core"),
    "data", "campaign", "rules.csv"
)
BATCH_SIZE = 50
COL_TEXT = 4  # column index for the text field in rules.csv

def main():
    print(f"Reading vanilla CSV: {VANILLA_CSV}")
    with open(VANILLA_CSV, "r", encoding="cp1252") as f:
        rows = list(csv.reader(f))

    # Extract non-empty text entries: [row_index, text]
    entries = []
    for i, row in enumerate(rows):
        if len(row) > COL_TEXT and row[COL_TEXT].strip():
            entries.append([i, row[COL_TEXT]])

    print(f"  Total rows: {len(rows)}")
    print(f"  Rows with text: {len(entries)}")

    # Split into batches
    num_batches = math.ceil(len(entries) / BATCH_SIZE)
    for b in range(num_batches):
        batch = entries[b * BATCH_SIZE : (b + 1) * BATCH_SIZE]
        filename = f"texts_batch_{b + 1}.json"
        filepath = os.path.join(BASE, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"  {filename}: {len(batch)} entries")

    print(f"\nDone: {num_batches} batches created.")

if __name__ == "__main__":
    main()

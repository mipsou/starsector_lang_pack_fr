#!/usr/bin/env python3
"""
Identify texts truncated at ~300 characters during the original batch extraction.
Compare batch_X_Y.json texts against the vanilla rules.csv to find truncations.
"""

import csv
import json
import os
import sys
from pathlib import Path

VANILLA_CSV = r"D:\Fractal Softworks\Starsector\starsector-core\data\campaign\rules.csv"
CAMPAIGN_DIR = Path(r"D:\Fractal Softworks\Starsector\mods\starsector_lang_pack_fr_private\.claude\worktrees\objective-bartik\data\campaign")
RETRANSLATE_DIR = CAMPAIGN_DIR / "retranslate_batches"
OUTPUT_FILE = CAMPAIGN_DIR / "truncated_texts.json"

BATCH_SIZE = 50  # texts per retranslation batch


def load_vanilla_csv(path):
    """Load vanilla rules.csv and return dict of row_index -> column 4 text."""
    rows = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) > 4:
                rows[i] = row[4]
    return rows


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Loading vanilla rules.csv...")
    vanilla = load_vanilla_csv(VANILLA_CSV)
    print(f"  Loaded {len(vanilla)} rows with column 4 text")

    # Find all batch files
    batch_files = sorted(CAMPAIGN_DIR.glob("batch_*_*.json"))
    print(f"  Found {len(batch_files)} batch files")

    truncated = []
    total_pairs = 0

    for batch_path in batch_files:
        batch_name = batch_path.name
        # Derive tr file name: batch_X_Y.json -> tr_X_Y.json
        tr_name = batch_name.replace("batch_", "tr_")
        tr_path = CAMPAIGN_DIR / tr_name

        batch_data = load_json(batch_path)
        # Load translation file if exists
        tr_data = {}
        if tr_path.exists():
            tr_list = load_json(tr_path)
            for pair in tr_list:
                tr_data[pair[0]] = pair[1]

        for pair in batch_data:
            row_index = pair[0]
            batch_text = pair[1]
            total_pairs += 1

            if row_index not in vanilla:
                continue

            full_text = vanilla[row_index]

            # Check if truncated: full text must start with batch text
            # (true prefix truncation, not just a different text)
            if len(batch_text) < len(full_text) and full_text.startswith(batch_text):
                current_french = tr_data.get(row_index, "")
                truncated.append({
                    "row_index": row_index,
                    "batch_file": batch_name,
                    "tr_file": tr_name,
                    "full_english": full_text,
                    "truncated_english": batch_text,
                    "current_french": current_french,
                    "full_length": len(full_text),
                    "truncated_length": len(batch_text),
                })

    print(f"\n=== RESULTS ===")
    print(f"Total text pairs checked: {total_pairs}")
    print(f"Truncated texts found: {len(truncated)}")

    if not truncated:
        print("No truncated texts found!")
        return

    # Stats
    avg_full = sum(t["full_length"] for t in truncated) / len(truncated)
    avg_trunc = sum(t["truncated_length"] for t in truncated) / len(truncated)
    max_full = max(t["full_length"] for t in truncated)
    min_trunc = min(t["truncated_length"] for t in truncated)

    print(f"Average full text length: {avg_full:.0f} chars")
    print(f"Average truncated length: {avg_trunc:.0f} chars")
    print(f"Max full text length: {max_full} chars")
    print(f"Min truncated length: {min_trunc} chars")
    print(f"Average chars lost: {avg_full - avg_trunc:.0f}")

    # Save truncated_texts.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(truncated, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {OUTPUT_FILE}")

    # Create retranslation batches
    RETRANSLATE_DIR.mkdir(exist_ok=True)
    retranslate_items = [[t["row_index"], t["full_english"]] for t in truncated]

    num_batches = (len(retranslate_items) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(num_batches):
        start = i * BATCH_SIZE
        end = min(start + BATCH_SIZE, len(retranslate_items))
        batch = retranslate_items[start:end]
        batch_path = RETRANSLATE_DIR / f"retranslate_batch_{i+1}.json"
        with open(batch_path, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)

    print(f"\nCreated {num_batches} retranslation batches in {RETRANSLATE_DIR}")
    for i in range(num_batches):
        start = i * BATCH_SIZE
        end = min(start + BATCH_SIZE, len(retranslate_items))
        print(f"  retranslate_batch_{i+1}.json: {end - start} texts")

    # Distribution by batch group
    print(f"\nDistribution by batch group:")
    from collections import Counter
    groups = Counter()
    for t in truncated:
        group = t["batch_file"].split("_")[1]
        groups[group] += 1
    for g in sorted(groups.keys(), key=int):
        print(f"  Batch group {g}: {groups[g]} truncated texts")


if __name__ == "__main__":
    main()

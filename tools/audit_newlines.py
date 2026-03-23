#!/usr/bin/env python3
"""Audit \n mismatches between batch_X_Y.json (EN) and tr_X_Y.json (FR)."""

import json
import os
import glob

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Find all batch files
    batch_files = sorted(glob.glob(os.path.join(base_dir, "batch_*_*.json")))

    total_texts = 0
    total_match = 0
    total_mismatch = 0
    mismatches = []
    missing_tr = []
    missing_indices = []

    for batch_path in batch_files:
        fname = os.path.basename(batch_path)
        # batch_X_Y.json -> tr_X_Y.json
        tr_fname = "tr_" + fname[len("batch_"):]
        tr_path = os.path.join(base_dir, tr_fname)

        if not os.path.exists(tr_path):
            missing_tr.append(fname)
            continue

        with open(batch_path, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        with open(tr_path, "r", encoding="utf-8") as f:
            fr_data = json.load(f)

        # Build dict from FR data by index
        fr_dict = {item[0]: item[1] for item in fr_data}

        for item in en_data:
            idx = item[0]
            en_text = item[1]

            if idx not in fr_dict:
                missing_indices.append((fname, idx))
                continue

            fr_text = fr_dict[idx]
            total_texts += 1

            en_count = en_text.count("\n")
            fr_count = fr_text.count("\n")

            if en_count == fr_count:
                total_match += 1
            else:
                total_mismatch += 1
                mismatches.append({
                    "file": fname,
                    "index": idx,
                    "en_newlines": en_count,
                    "fr_newlines": fr_count,
                    "diff": en_count - fr_count,
                    "en_excerpt": en_text[:80].replace("\n", "\\n"),
                    "fr_excerpt": fr_text[:80].replace("\n", "\\n"),
                })

    # Summary
    print("=" * 70)
    print("NEWLINE AUDIT: batch_X_Y.json (EN) vs tr_X_Y.json (FR)")
    print("=" * 70)
    print(f"Batch files found:     {len(batch_files)}")
    print(f"Missing TR files:      {len(missing_tr)}")
    if missing_tr:
        for f in missing_tr:
            print(f"  - {f}")
    print(f"Missing FR indices:    {len(missing_indices)}")
    print()
    print(f"Total texts checked:   {total_texts}")
    print(f"Matching \\n count:     {total_match}")
    print(f"Mismatching \\n count:  {total_mismatch}")
    print(f"Mismatch rate:         {total_mismatch/total_texts*100:.1f}%" if total_texts else "N/A")
    print()

    # Breakdown by severity
    if mismatches:
        minor = [m for m in mismatches if abs(m["diff"]) <= 2]
        major = [m for m in mismatches if abs(m["diff"]) > 2]
        fr_more = [m for m in mismatches if m["diff"] < 0]  # FR has MORE \n
        fr_fewer = [m for m in mismatches if m["diff"] > 0]  # FR has FEWER \n

        print(f"FR has FEWER \\n than EN:  {len(fr_fewer)}")
        print(f"FR has MORE \\n than EN:   {len(fr_more)}")
        print(f"Minor (off by 1-2):       {len(minor)}")
        print(f"Major (off by 3+):        {len(major)}")
        print()

        # Distribution of diffs
        from collections import Counter
        diff_dist = Counter(m["diff"] for m in mismatches)
        print("Distribution of (EN_count - FR_count):")
        for diff_val in sorted(diff_dist.keys()):
            label = f"FR has {abs(diff_val)} {'fewer' if diff_val > 0 else 'more'} \\n"
            print(f"  {diff_val:+d} ({label}): {diff_dist[diff_val]} texts")
        print()

        # Show all mismatches grouped by file
        print("=" * 70)
        print("DETAILED MISMATCHES")
        print("=" * 70)

        current_file = None
        for m in mismatches:
            if m["file"] != current_file:
                current_file = m["file"]
                print(f"\n--- {current_file} ---")

            print(f"  idx={m['index']:>5d}  EN:\\n={m['en_newlines']}  FR:\\n={m['fr_newlines']}  diff={m['diff']:+d}")
            print(f"    EN: {m['en_excerpt']}")
            print(f"    FR: {m['fr_excerpt']}")

if __name__ == "__main__":
    main()

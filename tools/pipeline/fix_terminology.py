#!/usr/bin/env python3
"""
Fix terminology across all tr_*.json translation files.
Applies standardized French terminology corrections.
"""

import json
import glob
import os
import re

# Order matters: more specific patterns first to avoid partial replacements
REPLACEMENTS = [
    # 1. Hegemonie -> Hégémonie (fix missing accent)
    ("Hegemonie", "Hégémonie"),
    # 2. Hegémonie -> Hégémonie (fix partial accent)
    ("Hegémonie", "Hégémonie"),

    # 3. Ligue Perséenne -> Ligue Persane
    ("Ligue Perséenne", "Ligue Persane"),
    ("ligue perséenne", "ligue persane"),  # lowercase variant

    # 4. Secteur Perséen -> Secteur Persan
    ("Secteur Perséen", "Secteur Persan"),
    ("secteur perséen", "secteur persan"),

    # 5. Secteur Persean -> Secteur Persan (English adjective left)
    ("Secteur Persean", "Secteur Persan"),
    ("secteur persean", "secteur persan"),

    # 6. Chemin de Ludd -> Voie de Ludd
    ("Chemin de Ludd", "Voie de Ludd"),
    ("chemin de Ludd", "voie de Ludd"),

    # 7. Sentier de Ludd -> Voie de Ludd
    ("Sentier de Ludd", "Voie de Ludd"),
    ("sentier de Ludd", "voie de Ludd"),

    # 8. Sentieristes -> Voilistes (plural first)
    ("Sentieristes", "Voilistes"),
    ("sentieristes", "voilistes"),
    ("Sentieriste", "Voiliste"),
    ("sentieriste", "voiliste"),

    # 10. Voilards -> Voilistes (plural first)
    ("Voilards", "Voilistes"),
    ("voilards", "voilistes"),
    ("Voilard", "Voiliste"),
    ("voilard", "voiliste"),

    # 9. Voiliers -> Voilistes (plural first, when meaning Pather)
    ("Voiliers", "Voilistes"),
    ("voiliers", "voilistes"),
    ("Voilier", "Voiliste"),
    ("voilier", "voiliste"),

    # 11. Brillez bien -> Brûlez bien
    ("Brillez bien", "Brûlez bien"),
    ("brillez bien", "brûlez bien"),

    # 12. ingérante -> nuisible, ingérant -> nuisible
    ("ingérante", "nuisible"),
    ("ingérant", "nuisible"),
    ("Ingérante", "Nuisible"),
    ("Ingérant", "Nuisible"),
]


def apply_replacements(text):
    """Apply all terminology replacements to a text string."""
    changes = []
    new_text = text
    for old, new in REPLACEMENTS:
        if old in new_text:
            count = new_text.count(old)
            new_text = new_text.replace(old, new)
            changes.append((old, new, count))
    return new_text, changes


def process_file(filepath):
    """Process a single tr_*.json file and return change count."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_changes = []
    modified = False

    for entry in data:
        # Each entry is [line_number, text]
        if isinstance(entry, list) and len(entry) == 2:
            line_num, text = entry
            if isinstance(text, str):
                new_text, changes = apply_replacements(text)
                if changes:
                    entry[1] = new_text
                    modified = True
                    for old, new, count in changes:
                        file_changes.append((line_num, old, new, count))

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    return file_changes


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(script_dir, "tr_*.json")
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} tr_*.json files to process.\n")

    total_changes = 0
    total_files_modified = 0
    change_summary = {}

    for filepath in files:
        filename = os.path.basename(filepath)
        changes = process_file(filepath)
        if changes:
            total_files_modified += 1
            file_change_count = sum(c[3] for c in changes)
            total_changes += file_change_count
            print(f"  {filename}: {file_change_count} correction(s)")
            for line_num, old, new, count in changes:
                label = f"{old} -> {new}"
                change_summary[label] = change_summary.get(label, 0) + count

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_changes} corrections in {total_files_modified} files")
    print(f"{'='*60}")
    print("\nBreakdown by replacement:")
    for label, count in sorted(change_summary.items(), key=lambda x: -x[1]):
        print(f"  {label}: {count}")


if __name__ == "__main__":
    main()

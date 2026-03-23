#!/usr/bin/env python3
"""
QA Terminology Consistency Checker for French translation of Starsector rules.csv.
Scans all tr_*.json files for untranslated English terms and inconsistent French translations.
"""

import json
import re
import glob
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN_DIR = os.path.join(BASE_DIR, "data", "campaign")

# Terms to check: (english_pattern, description, expected_french, bad_french_patterns)
# We use case-insensitive matching where appropriate

CHECKS = [
    {
        "name": "Hegemony",
        "english_patterns": [
            # Match "Hegemony" as a standalone word (not part of Hégémonie etc.)
            r'\bHegemony\b',
        ],
        "french_variants": [
            # Track which French variants are used
            (r"[Hh][ée]g[ée]monie", "Hégémonie/variant"),
        ],
        "notes": "Should be translated to French (Hégémonie). Track accent variants.",
    },
    {
        "name": "Luddic Church",
        "english_patterns": [
            r'\bLuddic Church\b',
        ],
        "french_variants": [
            (r"[ÉE]glise de Ludd", "Église de Ludd"),
            (r"[ÉE]glise [Ll]uddique", "Église luddique (wrong)"),
        ],
        "notes": "Should contain 'Ludd' in French translation.",
    },
    {
        "name": "Luddic Path",
        "english_patterns": [
            r'\bLuddic Path\b',
        ],
        "french_variants": [
            (r"Voie de Ludd", "Voie de Ludd (correct)"),
            (r"Chemin de Ludd", "Chemin de Ludd (wrong)"),
            (r"Sentier de Ludd", "Sentier de Ludd (wrong)"),
        ],
        "notes": "Should be 'Voie de Ludd'.",
    },
    {
        "name": "Persean League",
        "english_patterns": [
            r'\bPersean League\b',
        ],
        "french_variants": [
            (r"Ligue Pers[ée]enne", "Ligue Perséenne (wrong)"),
            (r"Ligue Persane", "Ligue Persane (correct)"),
        ],
        "notes": "Should be 'Ligue Persane', not 'Ligue Perséenne'.",
    },
    {
        "name": "Sindrian Diktat",
        "english_patterns": [
            r'\bSindrian Diktat\b',
        ],
        "french_variants": [
            (r"Diktat Sindrien", "Diktat Sindrien (correct)"),
            (r"Diktat [Ss]indri(?!en)", "Diktat Sindri* (wrong variant)"),
        ],
        "notes": "Should be 'Diktat Sindrien'.",
    },
    {
        "name": "Tri-Tachyon",
        "english_patterns": [],  # Tri-Tachyon should stay as-is, no English issue
        "french_variants": [
            (r"Tri-Tachyon", "Tri-Tachyon (correct, keep as-is)"),
        ],
        "notes": "Should remain 'Tri-Tachyon' unchanged.",
    },
    {
        "name": "Domain (untranslated)",
        "english_patterns": [
            # Match "Domain" not preceded by letters (standalone English word)
            # But exclude "Domaine" which is the correct French
            r'(?<![A-Za-zÀ-ÿ])Domain(?!e)(?![A-Za-zÀ-ÿ])',
        ],
        "french_variants": [
            (r"Domaine", "Domaine (correct)"),
        ],
        "notes": "Should be 'Domaine', not 'Domain'.",
    },
    {
        "name": "Sector (untranslated)",
        "english_patterns": [
            # Match "Sector" as English, but not "Secteur"
            r'(?<![A-Za-zÀ-ÿ])Sector(?![A-Za-zÀ-ÿ])',
        ],
        "french_variants": [
            (r"Secteur", "Secteur (correct)"),
        ],
        "notes": "Should be 'Secteur', not 'Sector'.",
    },
]


def scan_files():
    pattern = os.path.join(CAMPAIGN_DIR, "tr_*.json")
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} tr_*.json files to scan.\n")

    # Results storage
    english_issues = defaultdict(list)  # term_name -> [(file, line_no, snippet)]
    french_variant_counts = defaultdict(lambda: defaultdict(list))  # term_name -> variant_label -> [(file, line_no)]

    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"ERROR reading {filename}: {e}")
            continue

        for entry in data:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            line_no = entry[0]
            text = entry[1]
            if not isinstance(text, str):
                continue

            for check in CHECKS:
                term_name = check["name"]

                # Check for untranslated English terms
                for eng_pat in check["english_patterns"]:
                    for m in re.finditer(eng_pat, text):
                        # Extract context around the match
                        start = max(0, m.start() - 30)
                        end = min(len(text), m.end() + 30)
                        snippet = text[start:end].replace("\n", " ")
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(text):
                            snippet = snippet + "..."
                        english_issues[term_name].append((filename, line_no, snippet))

                # Check French variant usage
                for fr_pat, fr_label in check["french_variants"]:
                    if re.search(fr_pat, text):
                        french_variant_counts[term_name][fr_label].append((filename, line_no))

    # === REPORT ===
    print("=" * 80)
    print("TERMINOLOGY CONSISTENCY REPORT")
    print("=" * 80)

    total_issues = 0

    # 1. Untranslated English terms
    print("\n" + "=" * 80)
    print("SECTION 1: UNTRANSLATED ENGLISH TERMS FOUND IN FRENCH TEXT")
    print("=" * 80)

    for check in CHECKS:
        term_name = check["name"]
        issues = english_issues.get(term_name, [])
        if issues:
            total_issues += len(issues)
            print(f"\n--- {term_name}: {len(issues)} occurrence(s) ---")
            print(f"    Note: {check['notes']}")
            for filename, line_no, snippet in issues:
                print(f"    [{filename}] line {line_no}: {snippet}")
        elif check["english_patterns"]:
            print(f"\n--- {term_name}: OK (no untranslated occurrences) ---")

    # 2. French variant consistency
    print("\n" + "=" * 80)
    print("SECTION 2: FRENCH TRANSLATION VARIANTS FOUND")
    print("=" * 80)

    for check in CHECKS:
        term_name = check["name"]
        variants = french_variant_counts.get(term_name, {})
        if variants:
            print(f"\n--- {term_name} ---")
            print(f"    Note: {check['notes']}")
            for label, occurrences in sorted(variants.items(), key=lambda x: -len(x[1])):
                print(f"    {label}: {len(occurrences)} occurrence(s)")
                # Show first 5 examples
                for filename, line_no in occurrences[:5]:
                    print(f"        [{filename}] line {line_no}")
                if len(occurrences) > 5:
                    print(f"        ... and {len(occurrences) - 5} more")
        else:
            print(f"\n--- {term_name}: no French variants found ---")

    # 3. Hegemony accent analysis
    print("\n" + "=" * 80)
    print("SECTION 3: HEGEMONY ACCENT VARIANT ANALYSIS")
    print("=" * 80)

    heg_variants = defaultdict(list)
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            continue
        for entry in data:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            line_no = entry[0]
            text = entry[1]
            if not isinstance(text, str):
                continue
            for m in re.finditer(r'[HhLl][eéè]g[eéè]moni[eé]', text):
                variant = m.group()
                heg_variants[variant].append((filename, line_no))

    if heg_variants:
        for variant, occurrences in sorted(heg_variants.items(), key=lambda x: -len(x[1])):
            print(f"  '{variant}': {len(occurrences)} occurrence(s)")
            for fn, ln in occurrences[:3]:
                print(f"      [{fn}] line {ln}")
            if len(occurrences) > 3:
                print(f"      ... and {len(occurrences) - 3} more")
    else:
        print("  No Hégémonie variants found.")

    # 4. Persean Sector check
    print("\n" + "=" * 80)
    print("SECTION 4: 'PERSEAN SECTOR' / 'SECTEUR PERSEEN' VARIANTS")
    print("=" * 80)

    ps_variants = defaultdict(list)
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            continue
        for entry in data:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            line_no = entry[0]
            text = entry[1]
            if not isinstance(text, str):
                continue
            # Check for "Persean Sector" untranslated
            for m in re.finditer(r'Persean Sector', text):
                ps_variants["Persean Sector (EN)"].append((filename, line_no))
            # Check French variants
            for m in re.finditer(r'Secteur Pers[ée]en|Secteur Persan', text):
                ps_variants[m.group()].append((filename, line_no))

    if ps_variants:
        for variant, occurrences in sorted(ps_variants.items(), key=lambda x: -len(x[1])):
            print(f"  '{variant}': {len(occurrences)} occurrence(s)")
            for fn, ln in occurrences[:5]:
                print(f"      [{fn}] line {ln}")
            if len(occurrences) > 5:
                print(f"      ... and {len(occurrences) - 5} more")
    else:
        print("  No 'Persean Sector' variants found.")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total untranslated English terms found: {total_issues}")
    print(f"Files scanned: {len(files)}")


if __name__ == "__main__":
    scan_files()

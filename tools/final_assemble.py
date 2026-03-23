#!/usr/bin/env python3
"""
final_assemble.py — Reassemble rules.csv from vanilla + tr_*.json translations,
apply accent fixes and terminology fixes, then verify.
"""

import csv
import json
import re
import os
import glob
import io

VANILLA = r"D:\Fractal Softworks\Starsector\starsector-core\data\campaign\rules.csv"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(WORK_DIR, "rules.csv")

# ─── Step 1: Reassemble ─────────────────────────────────────────────

print("=== STEP 1: Reassemble ===")

# Read vanilla CSV
with open(VANILLA, "r", encoding="utf-8", errors="replace") as f:
    raw_vanilla = f.read()

reader = csv.reader(io.StringIO(raw_vanilla))
rows = list(reader)
vanilla_row_count = len(rows)
print(f"Vanilla CSV rows: {vanilla_row_count}")

# Load all tr_*.json files
tr_files = sorted(glob.glob(os.path.join(WORK_DIR, "tr_*.json")))
print(f"Translation files found: {len(tr_files)}")

translated_rows = set()
total_translations = 0

for tf in tr_files:
    with open(tf, "r", encoding="utf-8") as f:
        pairs = json.load(f)
    for row_idx, french_text in pairs:
        if row_idx < 0 or row_idx >= len(rows):
            print(f"  WARNING: row_idx {row_idx} out of range in {os.path.basename(tf)}")
            continue
        # Column 4 = text (0-indexed)
        if len(rows[row_idx]) > 4:
            rows[row_idx][4] = french_text
            translated_rows.add(row_idx)
            total_translations += 1

print(f"Total translation pairs applied: {total_translations}")
print(f"Unique rows translated: {len(translated_rows)}")

# Write assembled CSV
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)

print(f"Assembled CSV written to: {OUTPUT}")

# ─── Step 2: Accent fixes ───────────────────────────────────────────

print("\n=== STEP 2: Accent fixes ===")

# Re-read the assembled CSV
with open(OUTPUT, "r", encoding="utf-8") as f:
    assembled = f.read()

reader = csv.reader(io.StringIO(assembled))
rows = list(reader)

# Define accent fix groups - (pattern, replacement) using word boundaries
# We apply case-sensitive patterns
accent_fixes = []

# GROUP A
for src, dst in [
    ("etre", "être"), ("ete", "été"), ("etait", "était"), ("etais", "étais"),
    ("etaient", "étaient"), ("etes", "êtes"), ("etant", "étant"),
    ("deja", "déjà"), ("tres", "très"),
    ("desole", "désolé"), ("desolee", "désolée"),
    ("desoles", "désolés"), ("desolees", "désolées"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    # Also capitalized version
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

# GROUP B (-ière)
for src, dst in [
    ("maniere", "manière"), ("lumiere", "lumière"), ("derriere", "derrière"),
    ("premiere", "première"), ("derniere", "dernière"), ("entiere", "entière"),
    ("matiere", "matière"), ("carriere", "carrière"), ("frontiere", "frontière"),
    ("poussiere", "poussière"), ("priere", "prière"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

# GROUP C (-ème)
for src, dst in [
    ("systeme", "système"), ("probleme", "problème"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

# GROUP D (circumflex)
for src, dst in [
    ("controle", "contrôle"), ("diplome", "diplôme"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

accent_fixes.append((re.compile(r'\brole\b'), "rôle"))
accent_fixes.append((re.compile(r'\bRole\b'), "Rôle"))
accent_fixes.append((re.compile(r'\broles\b'), "rôles"))
accent_fixes.append((re.compile(r'\bRoles\b'), "Rôles"))
accent_fixes.append((re.compile(r'\bcote\b'), "côté"))
accent_fixes.append((re.compile(r'\bCote\b'), "Côté"))
accent_fixes.append((re.compile(r'\bcotes\b'), "côtés"))
accent_fixes.append((re.compile(r'\bCotes\b'), "Côtés"))
accent_fixes.append((re.compile(r'grace a '), "grâce à "))
accent_fixes.append((re.compile(r'Grace a '), "Grâce à "))
accent_fixes.append((re.compile(r'grace au'), "grâce au"))
accent_fixes.append((re.compile(r'Grace au'), "Grâce au"))

# GROUP E (-ité/-té)
for src, dst in [
    ("securite", "sécurité"), ("verite", "vérité"), ("societe", "société"),
    ("realite", "réalité"), ("capacite", "capacité"), ("liberte", "liberté"),
    ("qualite", "qualité"), ("opportunite", "opportunité"),
    ("necessite", "nécessité"), ("activite", "activité"),
    ("volonte", "volonté"), ("beaute", "beauté"), ("cruaute", "cruauté"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

# GROUP F (é- start)
for src, dst in [
    ("equipe", "équipe"), ("equipage", "équipage"), ("energie", "énergie"),
    ("etoile", "étoile"), ("etat", "état"), ("evenement", "événement"),
    ("etranger", "étranger"), ("etrangere", "étrangère"), ("epave", "épave"),
    ("equipement", "équipement"), ("echange", "échange"), ("eviter", "éviter"),
    ("ecraser", "écraser"), ("electronique", "électronique"),
    ("eliminer", "éliminer"), ("emission", "émission"),
]:
    accent_fixes.append((re.compile(r'\b' + src + r'\b'), dst))
    accent_fixes.append((re.compile(r'\b' + src.capitalize() + r'\b'), dst.capitalize()))

accent_count = 0
for i, row in enumerate(rows):
    if len(row) > 4 and i in translated_rows:
        text = row[4]
        for pattern, replacement in accent_fixes:
            text, n = pattern.subn(replacement, text)
            accent_count += n
        row[4] = text

print(f"Accent corrections applied: {accent_count}")

# Write after accent fixes
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)

# ─── Step 3: Terminology fixes ──────────────────────────────────────

print("\n=== STEP 3: Terminology fixes ===")

# Re-read
with open(OUTPUT, "r", encoding="utf-8") as f:
    assembled = f.read()
reader = csv.reader(io.StringIO(assembled))
rows = list(reader)

term_count = 0

def term_replace(text, old, new):
    global term_count
    count = text.count(old)
    if count > 0:
        term_count += count
        text = text.replace(old, new)
    return text

def term_replace_re(text, pattern, new):
    global term_count
    result, n = re.subn(pattern, new, text)
    term_count += n
    return result

for i, row in enumerate(rows):
    if len(row) > 4 and i in translated_rows:
        text = row[4]

        # Hegemonie → Hégémonie
        text = term_replace(text, "Hegemonie", "Hégémonie")
        text = term_replace(text, "Hegémonie", "Hégémonie")

        # Perséenne(s) → Persane(s), Perséen(s) → Persan(s)
        text = term_replace(text, "Perséennes", "Persanes")
        text = term_replace(text, "Perséenne", "Persane")
        text = term_replace(text, "Perséens", "Persans")
        text = term_replace(text, "Perséen", "Persan")

        # Perseane → Persane
        text = term_replace(text, "Perseane", "Persane")

        # Persean → Persan (only in translated rows, which we already filter)
        text = term_replace(text, "Persean", "Persan")

        # S-Sentier Luddique → V-Voie de Ludd (before broader patterns)
        text = term_replace(text, "S-Sentier Luddique", "V-Voie de Ludd")

        # Sentieriste(s) → Voiliste(s)
        text = term_replace(text, "Sentieristes", "Voilistes")
        text = term_replace(text, "Sentieriste", "Voiliste")

        # Voie Luddique → Voie de Ludd
        text = term_replace(text, "Voie Luddique", "Voie de Ludd")

        # Sentier Luddique → Voie de Ludd
        text = term_replace(text, "Sentier Luddique", "Voie de Ludd")

        # les/des/Les/Des Luddiques → les/des/Les/Des Luddics (noun usage)
        text = term_replace(text, "les Luddiques", "les Luddics")
        text = term_replace(text, "des Luddiques", "des Luddics")
        text = term_replace(text, "Les Luddiques", "Les Luddics")
        text = term_replace(text, "Des Luddiques", "Des Luddics")

        # luddique(s)/Luddique(s) → Luddic (adjective - remaining after noun patterns)
        text = term_replace(text, "luddiques", "Luddic")
        text = term_replace(text, "Luddiques", "Luddic")
        text = term_replace(text, "luddique", "Luddic")
        text = term_replace(text, "Luddique", "Luddic")

        row[4] = text

print(f"Terminology corrections applied: {term_count}")

# Write final
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)

print(f"Final CSV written to: {OUTPUT}")

# ─── Step 4: Verify ─────────────────────────────────────────────────

print("\n=== STEP 4: Verification ===")

# Re-read final
with open(OUTPUT, "r", encoding="utf-8") as f:
    final_raw = f.read()

reader = csv.reader(io.StringIO(final_raw))
final_rows = list(reader)

# Count raw lines
raw_lines = final_raw.count('\n')
if not final_raw.endswith('\n'):
    raw_lines += 1

print(f"Total CSV rows (parsed): {len(final_rows)}")
print(f"Vanilla CSV rows: {vanilla_row_count}")
print(f"Row count match: {'YES' if len(final_rows) == vanilla_row_count else 'NO - MISMATCH!'}")
print(f"Raw file lines: {raw_lines}")

# Verify header
print(f"\nLine 1 (header): {final_rows[0]}")

# Verify row 5 has French text
if len(final_rows) > 5:
    row5_text = final_rows[5][4] if len(final_rows[5]) > 4 else "(no col 4)"
    has_french = any(c in row5_text for c in "àâéèêëîïôùûüçÀÂÉÈÊËÎÏÔÙÛÜÇ")
    print(f"\nRow 5 text (first 120 chars): {row5_text[:120]}")
    print(f"Contains French characters: {has_french}")

# Check some OR separator / comment rows
print("\nSample comment/separator rows:")
for idx in [1, 2, 6]:  # These are typically comments or short rows
    if idx < len(final_rows):
        print(f"  Row {idx}: {final_rows[idx][:3] if len(final_rows[idx]) >= 3 else final_rows[idx]}")

# Count remaining bad terms
bad_terms = {
    "Hegemonie": 0,
    "Hegémonie": 0,
    "luddique": 0,
    "Luddique": 0,
    "Perseane": 0,
    "Sentieriste": 0,
    "Perséen": 0,
}

for i, row in enumerate(final_rows):
    if len(row) > 4 and i in translated_rows:
        text = row[4]
        for term in bad_terms:
            bad_terms[term] += text.count(term)

# Special: Hegemonie but not Hégémonie
# We need to check for "Hegemonie" that isn't "Hégémonie"
print(f"\nRemaining bad terms in translated rows:")
for term, count in bad_terms.items():
    status = "OK" if count == 0 else f"FOUND {count}!"
    print(f"  {term}: {status}")

print(f"\n=== DONE ===")
print(f"Accent corrections: {accent_count}")
print(f"Terminology corrections: {term_count}")
print(f"Rows translated: {len(translated_rows)}")

#!/usr/bin/env python
"""
integrate_and_assemble.py — One-pass pipeline:
1. Integrate retranslations into tr_*.json
2. Reassemble rules.csv from vanilla + all tr_*.json
3. Apply accent fixes on column 4
4. Apply terminology fixes on column 4
5. Verify output
"""

import json, csv, re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
VANILLA_CSV = r"D:\Fractal Softworks\Starsector\starsector-core\data\campaign\rules.csv"
RETRANS_DIR = os.path.join(BASE, "retranslate_batches")
OUTPUT_CSV = os.path.join(BASE, "rules.csv")

# ═══════════════════════════════════════════════════════════════
# STEP 1: Integrate retranslations into tr_*.json
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1: Integrate retranslations into tr_*.json")
print("=" * 60)

with open(os.path.join(BASE, "truncated_texts.json"), "r", encoding="utf-8") as f:
    truncated_texts = json.load(f)

row_to_tr = {entry["row_index"]: entry["tr_file"] for entry in truncated_texts}

# Load all tr_*.json
tr_data = {}
for p in sorted(glob.glob(os.path.join(BASE, "tr_*.json"))):
    fname = os.path.basename(p)
    with open(p, "r", encoding="utf-8") as f:
        tr_data[fname] = json.load(f)

# Index: fname -> {row_index: position}
tr_idx = {}
for fname, pairs in tr_data.items():
    tr_idx[fname] = {pair[0]: i for i, pair in enumerate(pairs)}

# Apply retranslations
retrans_count = 0
modified_files = set()
for n in range(1, 47):
    path = os.path.join(RETRANS_DIR, f"retranslate_tr_{n}.json")
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        retrans = json.load(f)
    for row_index, new_french in retrans:
        tr_file = row_to_tr.get(row_index)
        if not tr_file or tr_file not in tr_data:
            print(f"  WARN: row {row_index} -> tr_file not found")
            continue
        pos = tr_idx[tr_file].get(row_index)
        if pos is None:
            print(f"  WARN: row {row_index} not in {tr_file}")
            continue
        tr_data[tr_file][pos][1] = new_french
        modified_files.add(tr_file)
        retrans_count += 1

# Save modified tr files
for fname in sorted(modified_files):
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(tr_data[fname], f, ensure_ascii=False, indent=2)

print(f"  Retranslations integrated: {retrans_count}")
print(f"  tr_*.json files modified: {len(modified_files)}")

# ═══════════════════════════════════════════════════════════════
# STEP 2: Reassemble rules.csv
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 2: Reassemble rules.csv")
print("=" * 60)

with open(VANILLA_CSV, "r", encoding="cp1252") as f:
    rows = list(csv.reader(f))

print(f"  Vanilla rows: {len(rows)}")

# Merge all translations
replacements = {}
for pairs in tr_data.values():
    for row_index, french_text in pairs:
        replacements[row_index] = french_text

print(f"  Total translations: {len(replacements)}")

applied = 0
for ri, ft in replacements.items():
    if ri < len(rows) and len(rows[ri]) > 4:
        rows[ri][4] = ft
        applied += 1

print(f"  Applied to CSV: {applied}")

# ═══════════════════════════════════════════════════════════════
# STEP 3: Accent fixes (column 4 only)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 3: Accent fixes")
print("=" * 60)

ACCENT_FIXES = [
    (r'\betre\b', 'être'), (r'\bete\b', 'été'), (r'\betait\b', 'était'),
    (r'\betais\b', 'étais'), (r'\betaient\b', 'étaient'), (r'\betes\b', 'êtes'),
    (r'\betant\b', 'étant'),
    (r'\bdeja\b', 'déjà'), (r'\btres\b', 'très'),
    (r'\bdesole\b', 'désolé'), (r'\bdesolee\b', 'désolée'),
    (r'\bmaniere\b', 'manière'), (r'\blumiere\b', 'lumière'),
    (r'\bderriere\b', 'derrière'), (r'\bpremiere\b', 'première'),
    (r'\bderniere\b', 'dernière'), (r'\bentiere\b', 'entière'),
    (r'\bmatiere\b', 'matière'), (r'\bcarriere\b', 'carrière'),
    (r'\bfrontiere\b', 'frontière'), (r'\bpoussiere\b', 'poussière'),
    (r'\bpriere\b', 'prière'),
    (r'\bsysteme\b', 'système'), (r'\bprobleme\b', 'problème'),
    (r'\bcontrole\b', 'contrôle'), (r'\brole\b', 'rôle'), (r'\broles\b', 'rôles'),
    (r'\bdiplome\b', 'diplôme'), (r'\bcote\b', 'côté'), (r'\bcotes\b', 'côtés'),
    (r'grace a ', 'grâce à '), (r'grace au', 'grâce au'),
    (r'\bsecurite\b', 'sécurité'), (r'\bverite\b', 'vérité'),
    (r'\bsociete\b', 'société'), (r'\brealite\b', 'réalité'),
    (r'\bcapacite\b', 'capacité'), (r'\bliberte\b', 'liberté'),
    (r'\bqualite\b', 'qualité'), (r'\bopportunite\b', 'opportunité'),
    (r'\bnecessite\b', 'nécessité'), (r'\bactivite\b', 'activité'),
    (r'\bvolonte\b', 'volonté'), (r'\bbeaute\b', 'beauté'),
    (r'\bcruaute\b', 'cruauté'),
    (r'\bequipe\b', 'équipe'), (r'\bequipage\b', 'équipage'),
    (r'\benergie\b', 'énergie'), (r'\betoile\b', 'étoile'),
    (r'\betat\b', 'état'), (r'\bevenement\b', 'événement'),
    (r'\betranger\b', 'étranger'), (r'\betrangere\b', 'étrangère'),
    (r'\bepave\b', 'épave'), (r'\bequipement\b', 'équipement'),
    (r'\bechange\b', 'échange'), (r'\beviter\b', 'éviter'),
    (r'\belectronique\b', 'électronique'), (r'\beliminer\b', 'éliminer'),
    (r'\bemission\b', 'émission'),
]

accent_compiled = [(re.compile(p, re.IGNORECASE), r) for p, r in ACCENT_FIXES]

accent_total = 0
for row in rows:
    if len(row) > 4 and row[4]:
        text = row[4]
        for pat, repl in accent_compiled:
            text, n = pat.subn(repl, text)
            accent_total += n
        row[4] = text

print(f"  Accent fixes applied: {accent_total}")

# ═══════════════════════════════════════════════════════════════
# STEP 4: Terminology fixes (column 4 only)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 4: Terminology fixes")
print("=" * 60)

TERM_FIXES = [
    (re.compile(r'\bHegemonie\b'), 'Hégémonie'),
    (re.compile(r'\bHegémonie\b'), 'Hégémonie'),
    (re.compile(r'\bPerséennes\b'), 'Persanes'),
    (re.compile(r'\bPerséenne\b'), 'Persane'),
    (re.compile(r'\bPerséen\b'), 'Persan'),
    (re.compile(r'\bPerseane\b'), 'Persane'),
    (re.compile(r'\bSentieristes\b'), 'Voilistes'),
    (re.compile(r'\bSentieriste\b'), 'Voiliste'),
    # Voie de Ludd (before generic Luddique)
    (re.compile(r'\bVoie Luddique\b'), 'Voie de Ludd'),
    (re.compile(r'\bSentier Luddique\b'), 'Voie de Ludd'),
    # Noun: les/des Luddiques -> Luddics
    (re.compile(r'\b(les|des|Les|Des) [Ll]uddiques\b'), lambda m: f'{m.group(1)} Luddics'),
    # Adjective: luddiques/Luddiques -> Luddic
    (re.compile(r'\b[Ll]uddiques\b'), 'Luddic'),
    (re.compile(r'\b[Ll]uddique\b'), 'Luddic'),
]

term_total = 0
for row in rows:
    if len(row) > 4 and row[4]:
        text = row[4]
        for pat, repl in TERM_FIXES:
            matches = len(pat.findall(text))
            if matches:
                text = pat.sub(repl, text)
                term_total += matches
        row[4] = text

print(f"  Terminology fixes applied: {term_total}")

# Write output
with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\n  Output: {OUTPUT_CSV}")

# ═══════════════════════════════════════════════════════════════
# STEP 5: Verification
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 5: Verification")
print("=" * 60)

# Row count
ok_rows = len(rows) == 8369
print(f"  Row count: {len(rows)} (expected 8369) — {'OK' if ok_rows else 'MISMATCH!'}")

# Check truncated marker
marker = "Scanné et i"
truncated_found = sum(1 for r in rows if len(r) > 4 and marker in r[4])
if truncated_found == 0:
    print(f'  No "{marker}" truncation found — OK')
else:
    print(f'  WARNING: {truncated_found} truncated texts remain!')

print(f"  Accent fixes: {accent_total}")
print(f"  Terminology fixes: {term_total}")

# Sample 3 previously-truncated texts
print("\n  Sample previously-truncated texts (now complete):")
samples = [truncated_texts[0], truncated_texts[len(truncated_texts)//2], truncated_texts[-1]]
for s in samples:
    ri = s["row_index"]
    if ri < len(rows) and len(rows[ri]) > 4:
        t = rows[ri][4].replace("\n", "\\n")
        preview = t[:150] + "..." if len(t) > 150 else t
        print(f"    Row {ri} ({len(rows[ri][4])} chars): {preview}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

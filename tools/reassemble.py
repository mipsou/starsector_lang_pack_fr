#!/usr/bin/env python3
"""
Reassemble French translations into rules.csv from tr_*.json files.

Strategy: Parse the vanilla CSV raw text character-by-character to find exact
byte positions of column 4 for each CSV row. Then surgically replace column 4
content for translated rows, preserving ALL original formatting (line endings,
quoting style, etc.).

The tr_*.json indices are 0-based CSV row numbers (csv.reader output),
NOT raw file line numbers. Max index = 8368 (8369 rows total).
"""

import csv
import json
import glob
import io
import os
import re
import sys

WORKDIR = os.path.dirname(os.path.abspath(__file__))
VANILLA_PATH = r"D:\Fractal Softworks\Starsector\starsector-core\data\campaign\rules.csv"
OUTPUT_PATH = os.path.join(WORKDIR, "rules.csv")


def parse_csv_field_positions(raw_text):
    """
    Parse CSV raw text and return for each row: list of (start, end) char positions
    for each field, plus the row_end position.

    Returns: list of dicts, each with:
      - 'fields': list of (field_start, field_end) positions in raw_text
      - 'row_start': start position of the row
      - 'row_end': end position of the row (before the row-terminating \r\n or \n)
    """
    rows = []
    i = 0
    n = len(raw_text)

    while i < n:
        row_start = i
        fields = []

        while True:
            # Parse one field
            field_start = i

            if i < n and raw_text[i] == '"':
                # Quoted field — scan to closing quote
                # The field content is between the quotes
                i += 1  # skip opening quote
                content_start = i
                while i < n:
                    if raw_text[i] == '"':
                        if i + 1 < n and raw_text[i + 1] == '"':
                            # Escaped quote ""
                            i += 2
                        else:
                            # End of quoted field
                            content_end = i
                            i += 1  # skip closing quote
                            break
                    else:
                        i += 1
                else:
                    content_end = i  # unterminated quote

                fields.append((field_start, i))  # includes quotes
            else:
                # Unquoted field — scan to comma or line end
                while i < n and raw_text[i] not in (',', '\r', '\n'):
                    i += 1
                fields.append((field_start, i))

            # After field: comma (more fields), newline (end of row), or EOF
            if i < n and raw_text[i] == ',':
                i += 1  # skip comma, continue to next field
            else:
                # End of row
                row_end = i
                # Skip line ending
                if i < n and raw_text[i] == '\r':
                    i += 1
                if i < n and raw_text[i] == '\n':
                    i += 1

                rows.append({
                    'fields': fields,
                    'row_start': row_start,
                    'row_end': row_end,
                    'line_end': i,  # after \r\n
                })
                break

    return rows


def csv_quote_field(text, line_ending="\r\n"):
    """Quote a CSV field value, using the specified line ending for embedded newlines."""
    # Replace \n in text with the target line ending
    # The text from JSON has \n; we need \r\n in the CSV
    needs_quoting = (',' in text or '"' in text or '\n' in text or '\r' in text)
    if needs_quoting:
        # Escape internal quotes
        escaped = text.replace('"', '""')
        # Normalize newlines to target line ending
        escaped = escaped.replace('\r\n', '\n').replace('\r', '\n').replace('\n', line_ending)
        return '"' + escaped + '"'
    else:
        return text


# ═══════════════════════════════════════════════════════════
# STEP 1: Read vanilla CSV
# ═══════════════════════════════════════════════════════════
print("Step 1: Reading vanilla rules.csv...")
with open(VANILLA_PATH, "r", encoding="utf-8", errors="replace", newline="") as f:
    vanilla_raw = f.read()

vanilla_line_count = vanilla_raw.count("\n")
if not vanilla_raw.endswith("\n"):
    vanilla_line_count += 1
print(f"  Vanilla raw lines: {vanilla_line_count}")

# Also parse with csv.reader for reference
csv_reader = csv.reader(io.StringIO(vanilla_raw))
csv_rows = list(csv_reader)
print(f"  Vanilla CSV rows: {len(csv_rows)}")

# Detect line ending
if "\r\n" in vanilla_raw:
    line_ending = "\r\n"
elif "\r" in vanilla_raw:
    line_ending = "\r"
else:
    line_ending = "\n"
print(f"  Line ending: {repr(line_ending)}")

# ═══════════════════════════════════════════════════════════
# STEP 2: Parse field positions
# ═══════════════════════════════════════════════════════════
print("\nStep 2: Parsing CSV field positions...")
parsed_rows = parse_csv_field_positions(vanilla_raw)
print(f"  Parsed rows: {len(parsed_rows)}")

# Verify parsed row count matches csv.reader
if len(parsed_rows) != len(csv_rows):
    print(f"  WARNING: Parsed {len(parsed_rows)} rows but csv.reader found {len(csv_rows)}")
    # Try to find where they diverge
    for i in range(min(len(parsed_rows), len(csv_rows))):
        my_fields = len(parsed_rows[i]['fields'])
        csv_fields = len(csv_rows[i])
        if my_fields != csv_fields:
            print(f"  First divergence at row {i}: parsed {my_fields} fields, csv.reader {csv_fields}")
            break

# Verify field content matches csv.reader for a few rows
print("  Verifying field extraction...")
mismatches = 0
for test_idx in [0, 5, 6, 13, 100, 278]:
    if test_idx >= len(parsed_rows) or test_idx >= len(csv_rows):
        continue
    if len(parsed_rows[test_idx]['fields']) <= 4 or len(csv_rows[test_idx]) <= 4:
        continue

    # Extract field 4 raw text and decode it
    fs, fe = parsed_rows[test_idx]['fields'][4]
    raw_field = vanilla_raw[fs:fe]

    # Decode: if quoted, strip quotes and unescape ""
    if raw_field.startswith('"') and raw_field.endswith('"'):
        decoded = raw_field[1:-1].replace('""', '"')
    else:
        decoded = raw_field

    # Normalize newlines for comparison
    decoded_norm = decoded.replace('\r\n', '\n').replace('\r', '\n')
    expected_norm = csv_rows[test_idx][4].replace('\r\n', '\n').replace('\r', '\n')

    if decoded_norm != expected_norm:
        mismatches += 1
        print(f"  MISMATCH at row {test_idx}:")
        print(f"    Decoded: {repr(decoded_norm[:100])}")
        print(f"    Expected: {repr(expected_norm[:100])}")

if mismatches == 0:
    print(f"  All sample fields match csv.reader output.")

# ═══════════════════════════════════════════════════════════
# STEP 3: Load all tr_*.json translations
# ═══════════════════════════════════════════════════════════
print("\nStep 3: Loading tr_*.json files...")
tr_files = sorted(glob.glob(os.path.join(WORKDIR, "tr_*.json")))
print(f"  Found {len(tr_files)} translation files")

translations = {}  # row_idx -> french_text
for tr_file in tr_files:
    with open(tr_file, "r", encoding="utf-8") as f:
        entries = json.load(f)
    for row_idx, french_text in entries:
        translations[row_idx] = french_text

print(f"  Total unique translations: {len(translations)}")

# ═══════════════════════════════════════════════════════════
# STEP 4: Build accent/terminology fix functions
# ═══════════════════════════════════════════════════════════
print("\nStep 4: Preparing accent and terminology fixes...")

accent_patterns = []

def add_accent(pattern, replacement, label):
    accent_patterns.append((re.compile(pattern), replacement, label))

# GROUP A — Common words
add_accent(r'\betre\b', 'être', 'etre→être')
add_accent(r'\bEtre\b', 'Être', 'Etre→Être')
add_accent(r'\bete\b', 'été', 'ete→été')
add_accent(r'\bEte\b', 'Été', 'Ete→Été')
add_accent(r'\betait\b', 'était', 'etait→était')
add_accent(r'\bEtait\b', 'Était', 'Etait→Était')
add_accent(r'\betais\b', 'étais', 'etais→étais')
add_accent(r'\betaient\b', 'étaient', 'etaient→étaient')
add_accent(r'\bEtaient\b', 'Étaient', 'Etaient→Étaient')
add_accent(r'\betes\b', 'êtes', 'etes→êtes')
add_accent(r'\bEtes\b', 'Êtes', 'Etes→Êtes')
add_accent(r'\betant\b', 'étant', 'etant→étant')
add_accent(r'\bEtant\b', 'Étant', 'Etant→Étant')
add_accent(r'\bdeja\b', 'déjà', 'deja→déjà')
add_accent(r'\bDeja\b', 'Déjà', 'Deja→Déjà')
add_accent(r'\btres\b', 'très', 'tres→très')
add_accent(r'\bTres\b', 'Très', 'Tres→Très')
add_accent(r'\bdesole\b', 'désolé', 'desole→désolé')
add_accent(r'\bDesolé\b', 'Désolé', 'Desolé→Désolé')
add_accent(r'\bDesole\b', 'Désolé', 'Desole→Désolé')
add_accent(r'\bdesolee\b', 'désolée', 'desolee→désolée')
add_accent(r'\bdesoles\b', 'désolés', 'desoles→désolés')
add_accent(r'\bdesolees\b', 'désolées', 'desolees→désolées')

for word, accented in [
    ('maniere', 'manière'), ('lumiere', 'lumière'),
    ('derriere', 'derrière'), ('premiere', 'première'),
    ('derniere', 'dernière'), ('entiere', 'entière'),
    ('matiere', 'matière'), ('carriere', 'carrière'),
    ('frontiere', 'frontière'), ('poussiere', 'poussière'),
    ('priere', 'prière'),
]:
    add_accent(r'\b' + word + r'\b', accented, f'{word}→{accented}')
    cw = word[0].upper() + word[1:]
    ca = accented[0].upper() + accented[1:]
    add_accent(r'\b' + cw + r'\b', ca, f'{cw}→{ca}')
    add_accent(r'\b' + word + r's\b', accented + 's', f'{word}s→{accented}s')
    add_accent(r'\b' + cw + r's\b', ca + 's', f'{cw}s→{ca}s')

for word, accented in [('systeme', 'système'), ('probleme', 'problème')]:
    add_accent(r'\b' + word + r'\b', accented, f'{word}→{accented}')
    add_accent(r'\b' + word + r's\b', accented + 's', f'{word}s→{accented}s')
    cw = word[0].upper() + word[1:]
    ca = accented[0].upper() + accented[1:]
    add_accent(r'\b' + cw + r'\b', ca, f'{cw}→{ca}')
    add_accent(r'\b' + cw + r's\b', ca + 's', f'{cw}s→{ca}s')

add_accent(r'\bcontrole\b', 'contrôle', 'controle→contrôle')
add_accent(r'\bControle\b', 'Contrôle', 'Controle→Contrôle')
add_accent(r'\bcontroles\b', 'contrôles', 'controles→contrôles')
add_accent(r'\bcontroler\b', 'contrôler', 'controler→contrôler')
add_accent(r'\bcontrolee\b', 'contrôlée', 'controlee→contrôlée')
add_accent(r'\bcontrolees\b', 'contrôlées', 'controlees→contrôlées')
add_accent(r'\bcontrolez\b', 'contrôlez', 'controlez→contrôlez')
add_accent(r'\brole\b', 'rôle', 'role→rôle')
add_accent(r'\bRole\b', 'Rôle', 'Role→Rôle')
add_accent(r'\broles\b', 'rôles', 'roles→rôles')
add_accent(r'\bRoles\b', 'Rôles', 'Roles→Rôles')
add_accent(r'\bdiplome\b', 'diplôme', 'diplome→diplôme')
add_accent(r'\bdiplomes\b', 'diplômes', 'diplomes→diplômes')
add_accent(r'\bcote\b', 'côté', 'cote→côté')
add_accent(r'\bCote\b', 'Côté', 'Cote→Côté')
add_accent(r'\bcotes\b', 'côtés', 'cotes→côtés')
add_accent(r'\bgrace a\b', 'grâce à', 'grace a→grâce à')
add_accent(r'\bGrace a\b', 'Grâce à', 'Grace a→Grâce à')
add_accent(r'\bgrace au\b', 'grâce au', 'grace au→grâce au')
add_accent(r'\bGrace au\b', 'Grâce au', 'Grace au→Grâce au')

for word, accented in [
    ('securite', 'sécurité'), ('verite', 'vérité'),
    ('societe', 'société'), ('realite', 'réalité'),
    ('capacite', 'capacité'), ('liberte', 'liberté'),
    ('qualite', 'qualité'), ('opportunite', 'opportunité'),
    ('activite', 'activité'), ('volonte', 'volonté'),
    ('beaute', 'beauté'), ('cruaute', 'cruauté'),
]:
    add_accent(r'\b' + word + r'\b', accented, f'{word}→{accented}')
    add_accent(r'\b' + word + r's\b', accented + 's', f'{word}s→{accented}s')
    cw = word[0].upper() + word[1:]
    ca = accented[0].upper() + accented[1:]
    add_accent(r'\b' + cw + r'\b', ca, f'{cw}→{ca}')

add_accent(r'\bnecessite\b', 'nécessité', 'necessite→nécessité')
add_accent(r'\bNecessite\b', 'Nécessité', 'Necessite→Nécessité')
add_accent(r'\bnecessiter\b', 'nécessiter', 'necessiter→nécessiter')
add_accent(r'\bnecessitent\b', 'nécessitent', 'necessitent→nécessitent')
add_accent(r'\bnecessitait\b', 'nécessitait', 'necessitait→nécessitait')

group_f = [
    ('equipe', 'équipe'), ('equipes', 'équipes'),
    ('equipage', 'équipage'), ('equipages', 'équipages'),
    ('energie', 'énergie'), ('energies', 'énergies'),
    ('etoile', 'étoile'), ('etoiles', 'étoiles'),
    ('etat', 'état'), ('etats', 'états'),
    ('evenement', 'événement'), ('evenements', 'événements'),
    ('etranger', 'étranger'), ('etrangere', 'étrangère'),
    ('etrangers', 'étrangers'), ('etrangeres', 'étrangères'),
    ('epave', 'épave'), ('epaves', 'épaves'),
    ('equipement', 'équipement'), ('equipements', 'équipements'),
    ('eleve', 'élevé'), ('echange', 'échange'), ('echanges', 'échanges'),
    ('eviter', 'éviter'), ('ecraser', 'écraser'),
    ('electronique', 'électronique'), ('electroniques', 'électroniques'),
    ('eliminer', 'éliminer'), ('emission', 'émission'), ('emissions', 'émissions'),
]
for word, accented in group_f:
    add_accent(r'\b' + word + r'\b', accented, f'{word}→{accented}')
    cw = word[0].upper() + word[1:]
    ca = accented[0].upper() + accented[1:]
    add_accent(r'\b' + cw + r'\b', ca, f'{cw}→{ca}')

TERMINOLOGY = [
    ("Hegemonie", "Hégémonie"),
    ("Hegémonie", "Hégémonie"),
    ("Ligue Perséenne", "Ligue Persane"),
    ("ligue perséenne", "ligue persane"),
    ("Secteur Perséen", "Secteur Persan"),
    ("secteur perséen", "secteur persan"),
    ("Secteur Persean", "Secteur Persan"),
    ("secteur persean", "secteur persan"),
    ("Perséenne", "Persane"),
    ("perséenne", "persane"),
    ("Perséen", "Persan"),
    ("perséen", "persan"),
    ("Perseen", "Persan"),
    ("perseen", "persan"),
    ("Sentieristes", "Voilistes"),
    ("sentieristes", "voilistes"),
    ("Sentieriste", "Voiliste"),
    ("sentieriste", "voiliste"),
    ("Voie Luddique", "Voie de Ludd"),
    ("voie Luddique", "voie de Ludd"),
    ("Sentier Luddique", "Voie de Ludd"),
    ("sentier Luddique", "voie de Ludd"),
    ("Chemin de Ludd", "Voie de Ludd"),
    ("chemin de Ludd", "voie de Ludd"),
    ("Sentier de Ludd", "Voie de Ludd"),
    ("sentier de Ludd", "voie de Ludd"),
    ("Luddiques", "Luddics"),
    ("luddiques", "luddics"),
    ("Luddique", "Luddic"),
    ("luddique", "luddic"),
    ("Brulez bien", "Brûlez bien"),
    ("brulez bien", "brûlez bien"),
    ("Brillez bien", "Brûlez bien"),
    ("brillez bien", "brûlez bien"),
    ("ingérante", "nuisible"),
    ("ingérant", "nuisible"),
    ("Ingérante", "Nuisible"),
    ("Ingérant", "Nuisible"),
    ("Voilards", "Voilistes"),
    ("voilards", "voilistes"),
    ("Voilard", "Voiliste"),
    ("voilard", "voiliste"),
    ("Voiliers", "Voilistes"),
    ("voiliers", "voilistes"),
    ("Voilier", "Voiliste"),
    ("voilier", "voiliste"),
]


def apply_fixes(text):
    """Apply accent fixes and terminology corrections to a translation string."""
    for regex, replacement, label in accent_patterns:
        text = regex.sub(replacement, text)
    for old, new in TERMINOLOGY:
        text = text.replace(old, new)
    return text


# Apply fixes to all translations
total_accent_fixes = 0
total_term_fixes = 0
accent_counts = {}
term_counts = {}

for row_idx in list(translations.keys()):
    original = translations[row_idx]
    fixed = original

    # Accent fixes
    for regex, replacement, label in accent_patterns:
        count = len(regex.findall(fixed))
        if count > 0:
            fixed = regex.sub(replacement, fixed)
            total_accent_fixes += count
            accent_counts[label] = accent_counts.get(label, 0) + count

    # Terminology fixes
    for old, new in TERMINOLOGY:
        count = fixed.count(old)
        if count > 0:
            fixed = fixed.replace(old, new)
            total_term_fixes += count
            term_counts[f"{old} → {new}"] = term_counts.get(f"{old} → {new}", 0) + count

    translations[row_idx] = fixed

print(f"  Accent fixes applied: {total_accent_fixes}")
for label, count in sorted(accent_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"    {label}: {count}")
if len(accent_counts) > 10:
    print(f"    ... and {len(accent_counts) - 10} more patterns")

print(f"  Terminology fixes applied: {total_term_fixes}")
for label, count in sorted(term_counts.items(), key=lambda x: -x[1]):
    print(f"    {label}: {count}")

# ═══════════════════════════════════════════════════════════
# STEP 5: Build output by surgical replacement
# ═══════════════════════════════════════════════════════════
print("\nStep 5: Building output with surgical replacements...")

# We'll build the output by copying vanilla_raw but replacing field 4 content
# for translated rows.
#
# Strategy: Process rows in order. For each row, if it has a translation,
# replace field 4. Otherwise copy verbatim.

parts = []
last_pos = 0
applied = 0
errors = []

for row_idx in range(len(parsed_rows)):
    row_info = parsed_rows[row_idx]

    if row_idx not in translations:
        continue  # will copy verbatim

    if len(row_info['fields']) <= 4:
        errors.append(f"Row {row_idx} has only {len(row_info['fields'])} fields")
        continue

    french_text = translations[row_idx]

    # Get field 4 position
    f4_start, f4_end = row_info['fields'][4]

    # Copy everything before this field
    parts.append(vanilla_raw[last_pos:f4_start])

    # Write the French text as a properly quoted CSV field
    quoted = csv_quote_field(french_text, line_ending=line_ending)
    parts.append(quoted)

    # Move past the old field
    last_pos = f4_end
    applied += 1

# Copy any remaining text after the last replacement
parts.append(vanilla_raw[last_pos:])

output_text = "".join(parts)
print(f"  Applied: {applied}")
if errors:
    print(f"  Errors: {len(errors)}")
    for e in errors[:10]:
        print(f"    {e}")

# ═══════════════════════════════════════════════════════════
# STEP 6: Write final output
# ═══════════════════════════════════════════════════════════
print("\nStep 6: Writing final output...")
with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(output_text)

print(f"  Written to: {OUTPUT_PATH}")
print(f"  File size: {os.path.getsize(OUTPUT_PATH):,} bytes")

# ═══════════════════════════════════════════════════════════
# STEP 7: Verification
# ═══════════════════════════════════════════════════════════
print("\nStep 7: Verification...")

with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
    verify_raw = f.read()

verify_line_count = verify_raw.count("\n")
if not verify_raw.endswith("\n"):
    verify_line_count += 1
print(f"  Output raw lines: {verify_line_count}")
print(f"  Expected: {vanilla_line_count}")
if verify_line_count == vanilla_line_count:
    print("  LINE COUNT MATCHES!")
else:
    diff = verify_line_count - vanilla_line_count
    print(f"  LINE COUNT DIFFERENCE: {diff:+d}")
    print("  (This may be expected if French texts have different newline counts than English)")

# Parse back to verify CSV structure
verify_reader = csv.reader(io.StringIO(verify_raw))
verify_rows = list(verify_reader)
print(f"  Output CSV rows: {len(verify_rows)} (expected {len(csv_rows)})")
if len(verify_rows) == len(csv_rows):
    print("  CSV ROW COUNT MATCHES!")

# Spot-check translations
print("\n  Spot checks (translated rows):")
sample_translated = [5, 13, 32, 51, 100, 278, 280, 281]
for idx in sample_translated:
    if idx < len(verify_rows) and len(verify_rows[idx]) > 4:
        text = verify_rows[idx][4]
        is_french = any(c in text for c in 'àâéèêëîïôùûüçÀÂÉÈÊËÎÏÔÙÛÜÇ') or 'Votre' in text or 'vous' in text
        lang = 'FR' if is_french else 'EN?'
        print(f"    Row {idx}: {lang} — {text[:90]}")

print("\n  Spot checks (untranslated rows should be English):")
for idx in [1, 2, 3, 4]:
    if idx < len(verify_rows) and len(verify_rows[idx]) > 4:
        text = verify_rows[idx][4]
        print(f"    Row {idx}: {text[:90]}")

# Verify no translated row lost its translation
print(f"\n  Checking all {len(translations)} translations are present in output...")
missing = 0
for row_idx, french_text in translations.items():
    if row_idx < len(verify_rows) and len(verify_rows[row_idx]) > 4:
        # Compare normalized (accent/term fixes may have changed the text)
        actual = verify_rows[row_idx][4]
        # Just check it's not the original English
        original_english = csv_rows[row_idx][4] if row_idx < len(csv_rows) and len(csv_rows[row_idx]) > 4 else None
        if actual == original_english:
            missing += 1
            if missing <= 5:
                print(f"    WARNING: Row {row_idx} still has English text")

if missing == 0:
    print(f"  All {len(translations)} translations verified present!")
else:
    print(f"  WARNING: {missing} rows still have English text")

print("\n" + "=" * 60)
print("REASSEMBLY COMPLETE")
print("=" * 60)

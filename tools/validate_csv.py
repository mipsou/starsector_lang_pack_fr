#!/usr/bin/env python
"""Validateur CSV pour Starsector - détecte les bugs de parsing AVANT le lancement du jeu.

Starsector utilise un parser CSV non-standard :
- Chaque " toggle l'état in_quotes (pas d'échappement "")
- Un nombre IMPAIR de " dans le fichier = crash garanti
- Un champ texte non-quoté contenant une virgule = champs décalés = crash

Usage:
    python tools/validate_csv.py [fichier.csv ...]
    Sans argument: valide tous les CSV du mod.
"""

import sys
import re
import os
from pathlib import Path


VANILLA_ROOT = None


def find_vanilla_root():
    """Trouve le dossier starsector-core."""
    global VANILLA_ROOT
    if VANILLA_ROOT:
        return VANILLA_ROOT
    mod_root = Path(__file__).parent.parent
    # Remonter jusqu'à starsector-core
    for candidate in [
        mod_root.parent.parent / 'starsector-core',
        Path('D:/Fractal Softworks/Starsector/starsector-core'),
    ]:
        if candidate.exists():
            VANILLA_ROOT = candidate
            return VANILLA_ROOT
    return None


def parse_rows_toggle(content):
    """Parse CSV avec le toggle parser de Starsector. Retourne {row_id: (line, field_count)}."""
    rows = {}
    in_quotes = False
    fields = []
    field_buf = ''
    line_num = 1
    row_start = 1

    for c in content:
        if c == '"':
            in_quotes = not in_quotes
            field_buf += c
        elif c == ',' and not in_quotes:
            fields.append(field_buf)
            field_buf = ''
        elif c == '\n' and not in_quotes:
            fields.append(field_buf)
            row_id = fields[0].strip() if fields else ''
            if row_id and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', row_id):
                rows[row_id] = (row_start, len(fields))
            fields = []
            field_buf = ''
            row_start = line_num + 1
        else:
            field_buf += c
        if c == '\n':
            line_num += 1

    return rows


def validate_quote_parity(filepath):
    """Vérifie que le nombre total de guillemets est pair."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    count = content.count('"')
    if count % 2 != 0:
        return False, f"IMPAIR ({count} guillemets) - crash garanti"
    return True, f"OK ({count} guillemets, pair)"


def validate_vs_vanilla(filepath):
    """Compare le nombre de champs de chaque row avec le vanilla."""
    vanilla_root = find_vanilla_root()
    if not vanilla_root:
        return []

    mod_root = Path(__file__).parent.parent
    rel_path = Path(filepath).relative_to(mod_root)
    vanilla_path = vanilla_root.parent / 'mods' / '..' / 'starsector-core' / rel_path
    # Simplify
    vanilla_path = vanilla_root / rel_path
    if not vanilla_path.exists():
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        mod_content = f.read()
    try:
        with open(vanilla_path, 'r', encoding='utf-8') as f:
            van_content = f.read()
    except UnicodeDecodeError:
        with open(vanilla_path, 'r', encoding='cp1252') as f:
            van_content = f.read()

    mod_rows = parse_rows_toggle(mod_content)
    van_rows = parse_rows_toggle(van_content)

    issues = []
    for row_id, (mod_line, mod_fc) in mod_rows.items():
        if row_id in van_rows:
            van_line, van_fc = van_rows[row_id]
            if mod_fc != van_fc:
                issues.append((mod_line, row_id, mod_fc, van_fc))

    return issues


def validate_file(filepath):
    """Valide un fichier CSV."""
    name = os.path.basename(filepath)
    errors = []

    # Test 1: Parité des guillemets
    ok, msg = validate_quote_parity(filepath)
    if not ok:
        errors.append(f"  PARITÉ: {msg}")

    # Test 2: Comparaison field count vs vanilla
    issues = validate_vs_vanilla(filepath)
    for line, row_id, mod_fc, van_fc in issues:
        errors.append(f"  CHAMPS L{line}: {row_id} a {mod_fc} champs (vanilla={van_fc})")

    return errors


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        mod_root = Path(__file__).parent.parent
        files = []
        for pattern in [
            'data/campaign/rules.csv',
            'data/characters/skills/skill_data.csv',
            'data/characters/skills/aptitude_data.csv',
            'data/strings/descriptions.csv',
            'data/weapons/weapon_data.csv',
            'data/campaign/submarkets.csv',
        ]:
            p = mod_root / pattern
            if p.exists():
                files.append(str(p))

    total_errors = 0
    for filepath in files:
        errors = validate_file(filepath)
        status = "FAIL" if errors else "OK"
        print(f"[{status}] {os.path.basename(filepath)}")
        for e in errors:
            print(e)
        total_errors += len(errors)

    print(f"\n{'=' * 40}")
    if total_errors == 0:
        print("Tous les fichiers sont valides.")
    else:
        print(f"{total_errors} erreur(s) trouvée(s) !")
    return 1 if total_errors else 0


if __name__ == '__main__':
    sys.exit(main())

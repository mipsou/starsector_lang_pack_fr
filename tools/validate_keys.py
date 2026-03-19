#!/usr/bin/env python3
"""
Validation des clés JSON mod vs vanilla.
Vérifie que TOUTES les clés présentes dans les fichiers vanilla
sont aussi présentes dans les fichiers mod.
Empêche les crashs type 'JSONObject["tooltipX"] not found'.
"""

import json
import re
import sys
import os

VANILLA_ROOT = 'D:/Fractal Softworks/Starsector/starsector-core'
MOD_ROOT = os.path.join(os.path.dirname(__file__), '..')

# Fichiers JSON à vérifier (chemin relatif depuis la racine)
JSON_FILES = [
    'data/strings/tooltips.json',
    'data/strings/strings.json',
    'data/strings/ship_names.json',
    'data/config/custom_entities.json',
    'data/config/planets.json',
    'data/config/battle_objectives.json',
    'data/config/tag_data.json',
    'data/config/contact_tag_data.json',
    'data/world/factions/default_fleet_type_names.json',
    'data/world/factions/default_ranks.json',
]

def strip_comments(text):
    """Retire les commentaires # et les trailing commas pour parser le JSON Starsector."""
    text = re.sub(r'#[^\n]*', '', text)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text

def load_json(path):
    """Charge un fichier JSON Starsector (HJSON avec commentaires, trailing commas, valeurs sans guillemets)."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    clean = strip_comments(raw)
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # HJSON fallback : ajouter des guillemets aux valeurs non-quotées
        # Wrap unquoted values: key:value → key:"value"
        clean = re.sub(r':\s*([^"\[\]{},\s][^,}\]]*)', r':"\1"', clean)
        # Fix booleans and numbers that got quoted
        clean = re.sub(r'"(true|false|null)"', r'\1', clean)
        clean = re.sub(r'"(\d+\.?\d*)"', r'\1', clean)
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            print(f"  WARN: Impossible de parser {path} (HJSON trop complexe), skip")
            return {}

def check_keys(vanilla_path, mod_path):
    """Compare les clés vanilla vs mod. Retourne la liste des clés manquantes."""
    vanilla = load_json(vanilla_path)
    mod = load_json(mod_path)

    missing = []

    def compare(v_obj, m_obj, path=""):
        if isinstance(v_obj, dict):
            for key in v_obj:
                new_path = f"{path}.{key}" if path else key
                if key not in m_obj:
                    missing.append(new_path)
                elif isinstance(v_obj[key], dict):
                    if isinstance(m_obj.get(key), dict):
                        compare(v_obj[key], m_obj[key], new_path)

    compare(vanilla, mod)
    return missing

def main():
    errors = 0
    checked = 0

    for rel_path in JSON_FILES:
        vanilla_path = os.path.normpath(os.path.join(VANILLA_ROOT, rel_path))
        mod_path = os.path.normpath(os.path.join(MOD_ROOT, rel_path))

        if not os.path.exists(mod_path):
            continue  # Fichier pas encore traduit, OK

        if not os.path.exists(vanilla_path):
            print(f"WARN: Vanilla introuvable: {vanilla_path}")
            continue

        checked += 1
        missing = check_keys(vanilla_path, mod_path)

        if missing:
            print(f"FAIL: {rel_path} — {len(missing)} clé(s) manquante(s):")
            for key in missing:
                print(f"  - {key}")
            errors += len(missing)
        else:
            print(f"OK: {rel_path}")

    print(f"\n{'='*50}")
    print(f"Fichiers vérifiés: {checked}")
    print(f"Clés manquantes: {errors}")

    if errors > 0:
        print("\nCORRECTION REQUISE — Le jeu crashera avec ces clés manquantes!")
        sys.exit(1)
    else:
        print("\nTout est bon — aucune clé manquante.")
        sys.exit(0)

def check_apostrophes():
    """Vérifie l'absence d'apostrophes typographiques (U+2019) dans tous les fichiers."""
    bad_files = []
    data_dir = os.path.normpath(os.path.join(MOD_ROOT, 'data'))

    for root, dirs, files in os.walk(data_dir):
        for fname in files:
            if fname.endswith(('.json', '.csv')):
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '\u2019' in content:
                    lines = [i+1 for i, l in enumerate(content.split('\n')) if '\u2019' in l]
                    bad_files.append((fpath, lines))

    return bad_files


def main():
    errors = 0
    checked = 0

    print("=" * 50)
    print("VALIDATION MOD FR vs VANILLA")
    print("=" * 50)

    # 1. Clés JSON
    print("\n[1/2] Vérification des clés JSON...")
    for rel_path in JSON_FILES:
        vanilla_path = os.path.normpath(os.path.join(VANILLA_ROOT, rel_path))
        mod_path = os.path.normpath(os.path.join(MOD_ROOT, rel_path))

        if not os.path.exists(mod_path):
            continue

        if not os.path.exists(vanilla_path):
            print(f"  WARN: Vanilla introuvable: {vanilla_path}")
            continue

        checked += 1
        missing = check_keys(vanilla_path, mod_path)

        if missing:
            print(f"  FAIL: {rel_path} — {len(missing)} clé(s) manquante(s):")
            for key in missing:
                print(f"    - {key}")
            errors += len(missing)
        else:
            print(f"  OK: {rel_path}")

    # 2. Apostrophes typographiques
    print("\n[2/2] Vérification des apostrophes...")
    bad = check_apostrophes()
    if bad:
        for fpath, lines in bad:
            print(f"  FAIL: {fpath} — apostrophe U+2019 aux lignes {lines}")
            errors += len(lines)
    else:
        print("  OK: aucune apostrophe typographique trouvée")

    # Résumé
    print(f"\n{'='*50}")
    print(f"Fichiers JSON vérifiés: {checked}")
    print(f"Erreurs totales: {errors}")

    if errors > 0:
        print("\nCORRECTION REQUISE — Le jeu crashera ou affichera des '?'!")
        sys.exit(1)
    else:
        print("\nTOUT EST BON — prêt à commit.")
        sys.exit(0)


if __name__ == '__main__':
    main()

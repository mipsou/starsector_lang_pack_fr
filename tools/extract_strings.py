#!/usr/bin/env python3
"""
Script d'extraction des chaînes à traduire depuis les fichiers sources de Starsector.
Prépare les fichiers de traduction avec le contenu original en commentaire.
"""

import os
import json
import csv
from pathlib import Path
import codecs

# Chemins
STARSECTOR_CORE = "D:/Fractal Softworks/Starsector/starsector-core"
MOD_PATH = "D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr"

SOURCE_STRINGS = os.path.join(STARSECTOR_CORE, "data/strings")
TARGET_STRINGS = os.path.join(MOD_PATH, "localization/data/strings")

def ensure_dir(path):
    """Crée le dossier si il n'existe pas."""
    Path(path).mkdir(parents=True, exist_ok=True)

def detect_encoding(file_path):
    """Détecte l'encodage d'un fichier."""
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=enc) as f:
                f.read()
                return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # Par défaut

def extract_csv(source_file, target_file):
    """Extrait le contenu d'un fichier CSV et prépare le fichier de traduction."""
    encoding = detect_encoding(source_file)
    rows = []
    with open(source_file, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Créer le fichier de traduction
    with open(target_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # Ajouter une ligne de commentaire pour chaque entrée
        for row in rows:
            writer.writerow({k: f"# {v}" if k == 'text' else v for k, v in row.items()})

def extract_json(source_file, target_file):
    """Extrait le contenu d'un fichier JSON et prépare le fichier de traduction."""
    encoding = detect_encoding(source_file)
    with open(source_file, 'r', encoding=encoding) as f:
        data = json.load(f)

    # Créer le fichier de traduction
    translation_data = {}
    for key, value in data.items():
        translation_data[f"# {key}"] = value
        translation_data[key] = ""  # Espace pour la traduction

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(translation_data, f, ensure_ascii=False, indent=4)

def main():
    """Fonction principale."""
    ensure_dir(TARGET_STRINGS)

    print("Début de l'extraction...")

    # Traiter les fichiers CSV
    print("Traitement de descriptions.csv...")
    extract_csv(
        os.path.join(SOURCE_STRINGS, "descriptions.csv"),
        os.path.join(TARGET_STRINGS, "descriptions_fr.csv")
    )

    # Traiter les fichiers JSON
    json_files = ["ship_names.json", "strings.json", "tooltips.json"]
    for file in json_files:
        print(f"Traitement de {file}...")
        source = os.path.join(SOURCE_STRINGS, file)
        target = os.path.join(TARGET_STRINGS, file.replace('.json', '_fr.json'))
        extract_json(source, target)

    print("Extraction terminée. Les fichiers de traduction ont été préparés.")

if __name__ == "__main__":
    main()

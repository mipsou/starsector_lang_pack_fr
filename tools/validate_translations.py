#!/usr/bin/env python3
import os
import json
import csv
import chardet
import re
import sys
from pathlib import Path


class TranslationConfig:
    """Configuration de la traduction."""
    def __init__(self):
        self.base_dir = Path('D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private')
        self.localization_dir = self.base_dir / 'localization'
        self.data_dir = self.localization_dir / 'data'
        self.strings_dir = self.data_dir / 'strings'
        self.original_dir = self.base_dir / 'original'


class MissionValidator:
    """Validateur de missions et de typographie française."""

    # Caractères spéciaux typographie française
    GUILLEMET_OUVRANT = '\u00AB'  # «
    GUILLEMET_FERMANT = '\u00BB'  # »
    POINTS_SUSPENSION = '\u2026'  # …
    APOSTROPHE = '\u2019'         # '

    def __init__(self, config: TranslationConfig):
        self.config = config

    def validate_typography(self, text: str) -> bool:
        """
        Valide la typographie française d'un texte.

        Vérifie :
        - Pas de guillemets droits (")
        - Pas d'apostrophes droites (')
        - Espaces avant la ponctuation double (;:!?)
        - Espaces autour des guillemets français

        Args:
            text: Texte à valider

        Returns:
            True si la typographie est correcte, False sinon
        """
        # Vérifier les guillemets droits
        if '"' in text:
            return False

        # Vérifier les apostrophes droites
        if "'" in text:
            return False

        # Vérifier les espaces avant la ponctuation double
        if re.search(r'[^\s][;:!?]', text):
            return False

        # Vérifier les espaces autour des guillemets français
        if self.GUILLEMET_OUVRANT in text or self.GUILLEMET_FERMANT in text:
            if re.search(r'«[^\s\u202F]', text) or re.search(r'[^\s\u202F]»', text):
                return False

        return True


def check_encoding(file_path):
    """Vérifie l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        if result['encoding'].lower() != 'utf-8':
            print(f"ERREUR: {file_path} n'est pas en UTF-8 (détecté: {result['encoding']})")
            return False
    return True

def validate_json(file_path):
    """Valide un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except Exception as e:
        print(f"ERREUR: {file_path} - {str(e)}")
        return False

def validate_csv(file_path):
    """Valide un fichier CSV."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for i, row in enumerate(reader, 2):
                if len(row) != len(headers):
                    print(f"ERREUR: {file_path} ligne {i} - nombre de colonnes incorrect")
                    return False
        return True
    except Exception as e:
        print(f"ERREUR: {file_path} - {str(e)}")
        return False

def main():
    errors = False
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith(('_fr.json', '_fr.csv')):
                file_path = os.path.join(root, file)
                print(f"Validation de {file_path}...")
                
                if not check_encoding(file_path):
                    errors = True
                    continue
                
                if file.endswith('_fr.json'):
                    if not validate_json(file_path):
                        errors = True
                elif file.endswith('_fr.csv'):
                    if not validate_csv(file_path):
                        errors = True
    
    if errors:
        print("\nDes erreurs ont été trouvées. Veuillez les corriger.")
        sys.exit(1)
    else:
        print("\nTous les fichiers sont valides!")
        sys.exit(0)

if __name__ == '__main__':
    main()

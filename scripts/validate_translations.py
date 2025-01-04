#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import csv
import re
import sys
import chardet
import shutil
from pathlib import Path

# Force l'encodage en UTF-8 pour la sortie
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class TranslationConfig:
    """Configuration de la traduction."""
    def __init__(self):
        self.base_dir = Path('D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private')
        self.localization_dir = self.base_dir / 'localization'
        self.data_dir = self.localization_dir / 'data'
        self.strings_dir = self.data_dir / 'strings'
        self.missions_dir = self.data_dir / 'missions'

def check_encoding(file_path):
    """Vérifie l'encodage d'un fichier."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        print(f"ERREUR: {file_path} n'est pas en UTF-8")
        return False

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

def compare_with_original(translated_file, orig_file):
    """Compare la structure avec le fichier original."""
    translated_file = Path(translated_file)
    orig_file = Path(orig_file)
    
    if translated_file.suffix == '.json':
        with open(orig_file, 'r', encoding='utf-8') as f:
            orig = json.load(f)
        with open(translated_file, 'r', encoding='utf-8') as f:
            translated = json.load(f)
            
        # Vérifier que toutes les clés sont présentes
        orig_keys = set(_flatten_dict(orig))
        translated_keys = set(_flatten_dict(translated))
        
        missing = orig_keys - translated_keys
        extra = translated_keys - orig_keys
        
        if missing:
            print(f"ERREUR: Clés manquantes dans {translated_file}:")
            for key in missing:
                print(f"  - {key}")
        if extra:
            print(f"ERREUR: Clés supplémentaires dans {translated_file}:")
            for key in extra:
                print(f"  - {key}")
                
        return not (missing or extra)
    return True

def _flatten_dict(d, parent_key='', sep='.'):
    """Aplatit un dictionnaire pour comparer les clés."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class MissionValidator:
    """Validateur spécifique pour les fichiers de mission."""
    
    def __init__(self, config):
        self.config = config
        self.missions_dir = config.missions_dir
        
    def validate_typography(self, text):
        """Valide la typographie française."""
        errors = []
        
        # Vérifier les espaces avant la ponctuation
        if re.search(r'[^\s][;:!?»]', text):
            errors.append("Espace manquant avant ;:!?»")
        
        # Vérifier les espaces après «
        if re.search(r'«[^\s]', text):
            errors.append("Espace manquant après «")
        
        # Vérifier les guillemets français
        if re.search(r'["""]', text):
            errors.append("Utiliser les guillemets français « »")
        
        # Vérifier les points de suspension
        if "..." in text:
            errors.append("Utiliser le caractère points de suspension (…)")
        
        return len(errors) == 0

    def validate_mission_text(self, file_path):
        """Valide le fichier mission_text.txt."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # Validation de la structure
            if not content.startswith('Lieu :'):
                issues.append("Le fichier doit commencer par 'Lieu :'")
            
            # Validation de la typographie
            typo_issues = self.validate_typography(content)
            if not typo_issues:
                issues.append("Erreur de typographie")
            
            return issues
            
        except Exception as e:
            return [f"Erreur lors de la lecture du fichier : {str(e)}"]

def main():
    """Fonction principale."""
    config = TranslationConfig()
    errors = False
    mission_validator = MissionValidator(config)
    
    # Validation des fichiers de traduction
    for root, _, files in os.walk(config.strings_dir):
        for file in files:
            if not file.startswith('.'):  # Ignore les fichiers cachés
                file_path = Path(root) / file
                print(f"Validation de {file_path}...")
                
                # Trouver le fichier original correspondant
                rel_path = file_path.relative_to(config.localization_dir)
                orig_file = config.base_dir / 'original' / rel_path
                
                if not check_encoding(file_path):
                    errors = True
                    continue
                
                if file_path.suffix == '.json':
                    if not validate_json(file_path):
                        errors = True
                    elif orig_file.exists():
                        if not compare_with_original(file_path, orig_file):
                            errors = True
                elif file_path.suffix == '.csv':
                    if not validate_csv(file_path):
                        errors = True
    
    # Validation des fichiers de mission
    for root, _, files in os.walk(config.missions_dir):
        for file in files:
            if file == "mission_text.txt":
                file_path = Path(root) / file
                print(f"\nValidation de la mission : {file_path.parent.name}")
                issues = mission_validator.validate_mission_text(file_path)
                if issues:
                    errors = True
                    for issue in issues:
                        print(f"  - {issue}")
    
    if errors:
        print("\nDes erreurs ont été trouvées. Veuillez les corriger.")
        sys.exit(1)
    else:
        print("\nTous les fichiers sont valides!")
        sys.exit(0)

if __name__ == "__main__":
    main()

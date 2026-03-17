#!/usr/bin/env python3
import os
import json
import csv
import chardet
import sys

def check_encoding(file_path):
    """Vérifie l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        raw = f.read()
        # Si le fichier commence par BOM UTF-8, c'est bon
        if raw.startswith(b'\xef\xbb\xbf'):
            return True
        # Si le fichier est en ASCII, c'est compatible UTF-8
        result = chardet.detect(raw)
        print(f"Détection pour {file_path}: {result}")
        if result['encoding'] and result['encoding'].lower() in ['ascii', 'utf-8']:
            return True
        print(f"ERREUR: {file_path} n'est pas en UTF-8 (détecté: {result['encoding']})")
        return False

def validate_json(file_path):
    """Valide un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            # Ignorer les commentaires (lignes commençant par #)
            lines = [line for line in content.split('\n') if not line.strip().startswith('#')]
            content = '\n'.join(lines)
            json.loads(content)
        return True
    except Exception as e:
        print(f"ERREUR: {file_path} - {str(e)}")
        return False

def validate_csv(file_path):
    """Valide un fichier CSV."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
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

def compare_with_original(fr_file, orig_file):
    """Compare la structure avec le fichier original."""
    if fr_file.endswith('.json'):
        with open(orig_file, 'r', encoding='utf-8') as f:
            orig = json.load(f)
        with open(fr_file, 'r', encoding='utf-8') as f:
            fr = json.load(f)
            
        # Vérifier que toutes les clés sont présentes
        orig_keys = set(_flatten_dict(orig))
        fr_keys = set(_flatten_dict(fr))
        
        missing = orig_keys - fr_keys
        extra = fr_keys - orig_keys
        
        if missing:
            print(f"ERREUR: Clés manquantes dans {fr_file}:")
            for key in missing:
                print(f"  - {key}")
        if extra:
            print(f"ERREUR: Clés supplémentaires dans {fr_file}:")
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

def main():
    """Fonction principale."""
    errors = False
    
    for root, _, files in os.walk('localization'):
        for file in files:
            if file.endswith(('_fr.json', '_fr.csv')):
                file_path = os.path.join(root, file)
                print(f"\nValidation de {file_path}...")
                
                # Trouver le fichier original correspondant
                rel_path = os.path.relpath(file_path, 'localization')
                orig_file = os.path.join('original', rel_path.replace('_fr.', '.'))
                
                if not check_encoding(file_path):
                    errors = True
                    continue
                
                if file.endswith('_fr.json'):
                    if not validate_json(file_path):
                        errors = True
                    elif os.path.exists(orig_file):
                        if not compare_with_original(file_path, orig_file):
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

if __name__ == "__main__":
    main()

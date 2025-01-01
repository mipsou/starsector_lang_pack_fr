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

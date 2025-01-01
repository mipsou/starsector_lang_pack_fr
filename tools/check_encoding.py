#!/usr/bin/env python3
import os
import chardet
import sys

def check_file_encoding(file_path):
    """Vérifie l'encodage d'un fichier."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def main():
    errors = []
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith(('.json', '.csv', '.txt')):
                file_path = os.path.join(root, file)
                encoding = check_file_encoding(file_path)
                if encoding.lower() != 'utf-8':
                    errors.append(f"Erreur: {file_path} n'est pas en UTF-8 (détecté: {encoding})")
    
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("Tous les fichiers sont en UTF-8")
    sys.exit(0)

if __name__ == '__main__':
    main()

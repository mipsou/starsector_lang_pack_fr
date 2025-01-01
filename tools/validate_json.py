#!/usr/bin/env python3
import json
import os
import sys

def validate_json_file(file_path):
    """Valide un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json.load(file)
        return True
    except json.JSONDecodeError as e:
        print(f"Erreur dans {file_path}: {str(e)}")
        return False
    except Exception as e:
        print(f"Erreur inattendue dans {file_path}: {str(e)}")
        return False

def main():
    errors = []
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                if not validate_json_file(file_path):
                    errors.append(file_path)
    
    if errors:
        print(f"Erreurs dans les fichiers: {', '.join(errors)}")
        sys.exit(1)
    print("Tous les fichiers JSON sont valides")
    sys.exit(0)

if __name__ == '__main__':
    main()

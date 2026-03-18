#!/usr/bin/env python3
import csv
import os
import sys

def validate_csv_file(file_path):
    """Valide un fichier CSV."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Lecture des en-têtes
            expected_columns = len(headers)
            
            for line_num, row in enumerate(reader, 2):
                if len(row) != expected_columns:
                    print(f"Erreur ligne {line_num} dans {file_path}: {len(row)} colonnes au lieu de {expected_columns}")
                    return False
        return True
    except Exception as e:
        print(f"Erreur dans {file_path}: {str(e)}")
        return False

def main():
    errors = []
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                if not validate_csv_file(file_path):
                    errors.append(file_path)
    
    if errors:
        print(f"Erreurs dans les fichiers: {', '.join(errors)}")
        sys.exit(1)
    print("Tous les fichiers CSV sont valides")
    sys.exit(0)

if __name__ == '__main__':
    main()

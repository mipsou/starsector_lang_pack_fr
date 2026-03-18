#!/usr/bin/env python3
import os
import json
import csv
import shutil
from datetime import datetime

def backup_files():
    """Crée une sauvegarde des fichiers de traduction."""
    backup_dir = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(backup_dir, exist_ok=True)
    
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith(('_fr.json', '_fr.csv')):
                src = os.path.join(root, file)
                dst = os.path.join(backup_dir, os.path.relpath(src, 'data'))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    
    print(f"Sauvegarde créée dans {backup_dir}")

def update_json_files():
    """Met à jour les fichiers JSON de traduction."""
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith('.json') and not file.endswith('_fr.json'):
                src = os.path.join(root, file)
                dst = os.path.join(root, f"{os.path.splitext(file)[0]}_fr.json")
                
                if not os.path.exists(dst):
                    with open(src, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    with open(dst, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"Créé {dst}")

def update_csv_files():
    """Met à jour les fichiers CSV de traduction."""
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith('.csv') and not file.endswith('_fr.csv'):
                src = os.path.join(root, file)
                dst = os.path.join(root, f"{os.path.splitext(file)[0]}_fr.csv")
                
                if not os.path.exists(dst):
                    with open(src, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                    
                    with open(dst, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(rows)
                    print(f"Créé {dst}")

def main():
    print("Mise à jour des traductions...")
    backup_files()
    update_json_files()
    update_csv_files()
    print("Terminé!")

if __name__ == '__main__':
    main()

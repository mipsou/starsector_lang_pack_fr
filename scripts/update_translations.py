#!/usr/bin/env python3
import os
import json
import csv
import shutil
import codecs
import re
from datetime import datetime

def detect_encoding(file_path):
    """Détecte l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result['encoding']

def read_file_with_encoding(file_path):
    """Lit un fichier avec le bon encodage."""
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()

def backup_current_translations():
    """Sauvegarde les traductions actuelles."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f'localization.old/backup_{timestamp}'
    
    if os.path.exists('localization'):
        shutil.copytree('localization', backup_dir)
        print(f"Sauvegarde créée: {backup_dir}")

def clean_json_content(content):
    """Nettoie le contenu JSON pour le rendre valide."""
    # Supprimer les commentaires
    content = re.sub(r'^\s*#.*$', '', content, flags=re.MULTILINE)
    
    # Supprimer les virgules finales invalides
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Supprimer les lignes vides
    content = re.sub(r'\n\s*\n', '\n', content)
    
    return content

def create_fr_files():
    """Crée les fichiers de traduction français."""
    for root, _, files in os.walk('original'):
        for file in files:
            if file.endswith('.json'):
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, 'original')
                dst_dir = os.path.join('localization', os.path.dirname(rel_path))
                os.makedirs(dst_dir, exist_ok=True)
                
                base, ext = os.path.splitext(file)
                dst = os.path.join(dst_dir, f"{base}_fr{ext}")
                
                if not os.path.exists(dst):
                    # Lecture et nettoyage du JSON
                    with open(src, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = clean_json_content(content)
                    
                    # Écriture avec BOM UTF-8
                    with open(dst, 'wb') as f:
                        f.write(codecs.BOM_UTF8)
                        f.write(content.encode('utf-8'))
                    print(f"Créé: {dst} (UTF-8 with BOM)")
            
            elif file.endswith('.csv'):
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, 'original')
                dst_dir = os.path.join('localization', os.path.dirname(rel_path))
                os.makedirs(dst_dir, exist_ok=True)
                
                base, ext = os.path.splitext(file)
                dst = os.path.join(dst_dir, f"{base}_fr{ext}")
                
                if not os.path.exists(dst):
                    # Lecture et écriture du CSV avec BOM UTF-8
                    with open(src, 'r', encoding='utf-8') as f:
                        content = f.read()
                    with open(dst, 'wb') as f:
                        f.write(codecs.BOM_UTF8)
                        f.write(content.encode('utf-8'))
                    print(f"Créé: {dst} (UTF-8 with BOM)")

def main():
    """Fonction principale."""
    print("Mise à jour des traductions...")
    backup_current_translations()
    create_fr_files()
    print("Terminé!")

if __name__ == "__main__":
    main()

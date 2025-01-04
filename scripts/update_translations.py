#!/usr/bin/env python3
import os
import json
import csv
import shutil
import codecs
import re
import chardet
from datetime import datetime
from pathlib import Path

class TranslationConfig:
    """Configuration de la traduction."""
    def __init__(self):
        self.base_dir = Path('D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private')
        self.localization_dir = self.base_dir / 'localization'
        self.data_dir = self.localization_dir / 'data'
        self.strings_dir = self.data_dir / 'strings'
        self.original_dir = self.base_dir / 'original'

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

def backup_current_translations(config):
    """Sauvegarde les traductions actuelles."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = config.base_dir / f'localization.old/backup_{timestamp}'
    
    if config.localization_dir.exists():
        shutil.copytree(config.localization_dir, backup_dir)
        print(f"Sauvegarde créée: {backup_dir}")

def clean_json_content(content):
    """Nettoie le contenu JSON pour le rendre valide."""
    # Supprimer les commentaires ligne par ligne
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Supprimer les commentaires en fin de ligne
        comment_pos = line.find('#')
        if comment_pos >= 0:
            line = line[:comment_pos].rstrip()
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Supprimer les virgules finales invalides
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Supprimer les lignes vides
    content = '\n'.join(line for line in content.split('\n') if line.strip())
    
    return content

def create_translation_files(config):
    """Crée les fichiers de traduction."""
    for src_file in config.original_dir.rglob('*'):
        if src_file.is_file() and src_file.suffix in ['.json', '.csv']:
            # Calcul des chemins
            rel_path = src_file.relative_to(config.original_dir)
            dst_file = config.localization_dir / rel_path
            
            # Création du répertoire de destination
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            if not dst_file.exists():
                # Lecture et traitement du contenu
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if src_file.suffix == '.json':
                    content = clean_json_content(content)
                
                # Écriture avec BOM UTF-8
                with open(dst_file, 'wb') as f:
                    f.write(codecs.BOM_UTF8)
                    f.write(content.encode('utf-8'))
                print(f"Créé: {dst_file} (UTF-8 with BOM)")

def main():
    """Fonction principale."""
    config = TranslationConfig()
    
    print("Sauvegarde des traductions existantes...")
    backup_current_translations(config)
    
    print("\nCréation des fichiers de traduction...")
    create_translation_files(config)
    
    print("\nMise à jour terminée!")

if __name__ == "__main__":
    main()

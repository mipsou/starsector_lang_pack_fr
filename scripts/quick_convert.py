#!/usr/bin/env python3
"""
Script de conversion rapide des fichiers de traduction

Ce script :
- Copie les fichiers sources depuis le dossier original
- Crée les fichiers de traduction avec le suffixe _fr
- Vérifie l'encodage et le format des fichiers
- Applique les règles typographiques françaises

Auteur: Mipsou
Date: 2025-01-22
"""
import os
import shutil
from pathlib import Path
from utils import check_encoding, format_starsector_json, fix_quotes

def quick_convert():
    """Conversion rapide des fichiers."""
    try:
        # Mise à jour des fichiers sources
        os.system('python scripts/update_original.py')
        
        # Création des fichiers de traduction
        original_dir = Path('original/data/strings')
        for file_path in original_dir.rglob('*.*'):
            if file_path.is_file():
                # Calcul des chemins source et destination
                rel_path = file_path.relative_to(original_dir)
                dst_dir = Path('localization') / rel_path.parent
                dst_dir.mkdir(parents=True, exist_ok=True)
                
                # Création du nom de fichier avec suffixe _fr
                dst_name = f"{file_path.stem}_fr{file_path.suffix}"
                dst_path = dst_dir / dst_name
                
                if not dst_path.exists():
                    # Vérification de l'encodage du fichier source
                    if not check_encoding(file_path):
                        print(f"Attention : {file_path} n'est pas en UTF-8")
                        continue
                    
                    # Traitement spécifique selon le type de fichier
                    if file_path.suffix == '.json':
                        # Lecture et formatage du JSON
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Correction des guillemets et formatage
                        content = fix_quotes(content)
                        with open(dst_path, 'w', encoding='utf-8', newline='\n') as f:
                            f.write(content)
                            
                    else:
                        # Copie simple pour les autres types de fichiers
                        shutil.copy2(file_path, dst_path)
                    
                    print(f"Créé : {dst_path}")
                    
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    quick_convert()

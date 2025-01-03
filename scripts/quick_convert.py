#!/usr/bin/env python3
import os, shutil

def quick_convert():
    """Conversion rapide des fichiers."""
    # Copier les fichiers sources
    os.system('python scripts/update_original.py')
    
    # Créer les fichiers de traduction
    for root, _, files in os.walk('original/data/strings'):
        for file in files:
            src = os.path.join(root, file)
            dst_dir = os.path.join('localization', os.path.relpath(root, 'original'))
            os.makedirs(dst_dir, exist_ok=True)
            
            base, ext = os.path.splitext(file)
            dst = os.path.join(dst_dir, f"{base}_fr{ext}")
            
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"Créé: {dst}")

if __name__ == "__main__":
    quick_convert()

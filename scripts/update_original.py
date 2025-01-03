#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

STARSECTOR_CORE = "D:/Fractal Softworks/Starsector/starsector-core"
ORIGINAL_DIR = "original"
DATA_PATHS = [
    "data/strings/strings.json",
    "data/strings/descriptions.csv",
    "data/strings/ship_names.json",
    "data/strings/tooltips.json",
    "data/config/industries.json",
    "data/config/variants.json"
]

def copy_original_files():
    """Copie les fichiers originaux du jeu."""
    for path in DATA_PATHS:
        src = os.path.join(STARSECTOR_CORE, path)
        if not os.path.exists(src):
            print(f"ATTENTION: Fichier source manquant: {src}")
            continue

        dst = os.path.join(ORIGINAL_DIR, path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        shutil.copy2(src, dst)
        print(f"Copié: {path}")

if __name__ == "__main__":
    copy_original_files()

#!/usr/bin/env python3
"""
Validation des fichiers JSON.
"""

from pathlib import Path
from utils import validate_json_file

def main():
    """Point d'entrée principal."""
    # Fichiers à valider
    files = [
        Path("data/strings/strings.json"),
        Path("data/strings/tips.json"),
        Path("data/strings/tooltips.json")
    ]
    
    # Valider chaque fichier
    for file_path in files:
        print(f"\n=== Validation de {file_path} ===")
        valid, errors = validate_json_file(file_path)
        
        if valid:
            print("✅ Fichier valide")
        else:
            print("❌ Fichier invalide :")
            for error in errors:
                print(f"  - {error}")

if __name__ == "__main__":
    main()

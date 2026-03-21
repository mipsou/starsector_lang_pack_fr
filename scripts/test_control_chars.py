#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Ajouter le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import find_control_chars_binary

def main():
    # Test sur un fichier JSON
    test_file = '../data/strings/strings.json'
    print(f"Test de find_control_chars_binary sur {test_file}")
    find_control_chars_binary(test_file)
    
    # Vérifier que le log a été créé dans le bon dossier
    expected_log = '../logs/strings.json.control_chars.log'
    if os.path.exists(expected_log):
        print(f"\nFichier log créé avec succès dans : {expected_log}")
    else:
        print(f"\nERREUR: Le fichier log n'a pas été créé dans : {expected_log}")

if __name__ == '__main__':
    main()

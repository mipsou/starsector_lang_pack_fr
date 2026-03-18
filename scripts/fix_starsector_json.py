#!/usr/bin/env python3
"""
Script pour convertir les fichiers JSON au format spécifique de Starsector

Ce script normalise les fichiers JSON selon les conventions Starsector :
- Format JSON spécifique
- Encodage UTF-8
- Sauts de ligne Unix

Auteur: Mipsou
Date: 2025-01-22
"""
import json
import sys
import os
from pathlib import Path
import unittest

# Ajout du répertoire des scripts au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from utils import (format_starsector_json, check_encoding,
                  detect_file_format, format_file)

def fix_starsector_format(input_file, output_file=None, strict=True):
    """Convertit un fichier JSON au format Starsector.
    
    Args:
        input_file (str): Chemin du fichier à convertir
        output_file (str, optional): Chemin du fichier de sortie. Si None, écrase le fichier d'entrée.
        strict (bool): Si True, vérifie strictement l'encodage UTF-8
        
    Returns:
        bool: True si la conversion a réussi, False sinon
    """
    input_file = Path(input_file)
    output_file = Path(output_file) if output_file else input_file
    
    try:
        # Vérification du format
        file_format = detect_file_format(input_file)
        if not file_format.startswith('json_'):
            raise ValueError(f"Le fichier {input_file} n'est pas un fichier JSON valide")
        
        # Vérification de l'encodage
        if not check_encoding(input_file, strict=strict):
            raise ValueError(f"Le fichier {input_file} n'est pas en UTF-8")
        
        # Lecture du fichier JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        
        # Formatage selon les conventions Starsector
        formatted_json = format_starsector_json(data)
        
        # Application du formatage spécifique au type de fichier
        final_content = format_file(input_file, formatted_json)
        
        # Écriture du résultat
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(final_content)
            
        print(f"Fichier {output_file} formaté avec succès.")
        return True
            
    except Exception as e:
        print(f"Erreur : {str(e)}", file=sys.stderr)
        return False

class TestStarsectorFormat(unittest.TestCase):
    """Tests unitaires pour le formatage JSON Starsector."""
    
    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = Path("tests")
        self.test_file = self.test_dir / "test_format.json"
        self.output_file = self.test_dir / "test_format_out.json"
        self.test_dir.mkdir(exist_ok=True)
        
        # Création d'un fichier de test
        test_data = {
            "tips": [
                "Test tip 1",
                {"freq": 2, "tip": "Test tip 2"}
            ]
        }
        
        # Écriture avec l'encodage UTF-8 et newline='\n'
        with open(self.test_file, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(test_data, f, indent=4, ensure_ascii=False)
    
    def tearDown(self):
        """Nettoyage après les tests."""
        if self.test_file.exists():
            self.test_file.unlink()
        if self.output_file.exists():
            self.output_file.unlink()
        if self.test_dir.exists() and not any(self.test_dir.iterdir()):
            self.test_dir.rmdir()
    
    def test_format_conversion(self):
        """Teste la conversion du format."""
        # Test du format initial
        file_format = detect_file_format(self.test_file)
        self.assertTrue(file_format.startswith('json_'))
        
        # Test de la conversion avec mode permissif
        self.assertTrue(fix_starsector_format(self.test_file, self.output_file, strict=False))
        self.assertTrue(self.output_file.exists())
        
        # Vérification du contenu
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('tips:[', content)
            self.assertIn('"freq":', content)
            self.assertIn('"tip":', content)
        
        # Test de l'encodage
        self.assertTrue(check_encoding(self.output_file, strict=False))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=['dummy'])
    else:
        if len(sys.argv) < 2:
            print("Usage: python fix_starsector_json.py input_file [output_file]")
            sys.exit(1)
            
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not fix_starsector_format(input_file, output_file):
            sys.exit(1)

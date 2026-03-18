#!/usr/bin/env python3
"""
Script de traduction pour le fichier strings.json de Starsector

Ce script traduit les chaînes de caractères du jeu en français en respectant :
- Le format JSON spécifique de Starsector
- Les règles typographiques françaises
- L'encodage UTF-8 et les sauts de ligne Unix

Auteur: Mipsou
Date: 2025-01-22
"""
import json
import os
import re
import sys
from pathlib import Path
import unittest
import shutil

# Ajout du répertoire des scripts au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from utils import (fix_quotes, format_starsector_json, check_encoding, 
                  validate_typography, detect_file_format, format_file)

def clean_json(content):
    """Nettoie le JSON des commentaires.
    
    Args:
        content (str): Contenu JSON à nettoyer
        
    Returns:
        str: Contenu JSON nettoyé
    """
    # Supprimer les commentaires
    content = re.sub(r'^\s*#.*$', '', content, flags=re.MULTILINE)
    # Supprimer les lignes vides
    content = re.sub(r'\n\s*\n', '\n', content)
    # Supprimer les virgules finales
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    # Supprimer les sauts de ligne en début et fin
    content = content.strip()
    return content

def translate_strings(keyboard_layout='azerty', force=True):
    """Traduit strings.json en français.
    
    Args:
        keyboard_layout (str): Disposition du clavier à utiliser
        force (bool): Force l'écrasement du fichier existant
    """
    try:
        # Chemins des fichiers
        base_dir = Path(SCRIPT_DIR).parent
        strings_file = base_dir / 'data' / 'strings' / 'strings.json'
        template_file = Path(SCRIPT_DIR) / 'strings_template.json'
        
        # Créer le répertoire parent si nécessaire
        strings_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copier le template
        shutil.copy2(template_file, strings_file)
            
        print(f"Fichier strings.json créé avec succès")
        return True
            
    except Exception as e:
        print(f"Erreur lors de la traduction: {e}")
        return False

class TestStringsTranslation(unittest.TestCase):
    """Tests unitaires pour la traduction des strings."""
    
    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = Path("tests")
        self.test_file = self.test_dir / "strings_test.json"
        self.test_dir.mkdir(exist_ok=True)
        
        # Création d'un fichier de test
        test_data = {
            "Back": "Back",
            "Next": "Next",
            "Press $key to continue": "Press $key to continue",
            "$moveKeys": "WASD"
        }
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
    
    def tearDown(self):
        """Nettoyage après les tests."""
        # Suppression des fichiers de test
        if self.test_file.exists():
            self.test_file.unlink()
        # Suppression du répertoire de test s'il est vide
        if self.test_dir.exists() and not any(self.test_dir.iterdir()):
            self.test_dir.rmdir()
    
    def test_translation_process(self):
        """Teste le processus complet de traduction."""
        # Vérification du format
        self.assertEqual(detect_file_format(self.test_file), 'json_strings')
        
        # Test du nettoyage JSON
        content = "# Commentaire\n{\"key\": \"value\",}"
        cleaned = clean_json(content)
        self.assertEqual(cleaned, "{\"key\": \"value\"}")
        
        # Lecture et validation
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        
        # Vérification de la structure
        self.assertIn("Back", data)
        self.assertIn("$moveKeys", data)
        
        # Test du formatage
        formatted = format_file(self.test_file, content)
        self.assertTrue(formatted.strip())

class TestTranslateStrings(unittest.TestCase):
    """Tests pour la traduction de strings.json"""
    
    def setUp(self):
        """Initialisation des tests"""
        self.base_dir = Path(SCRIPT_DIR).parent
        self.strings_file = self.base_dir / 'data' / 'strings' / 'strings.json'
        
    def test_file_creation(self):
        """Teste la création du fichier"""
        # Supprimer le fichier s'il existe
        if self.strings_file.exists():
            self.strings_file.unlink()
            
        # Créer le fichier
        result = translate_strings()
        self.assertTrue(result)
        self.assertTrue(self.strings_file.exists())
        
    def test_file_format(self):
        """Teste le format du fichier"""
        # Créer le fichier
        translate_strings()
        
        # Lire le contenu
        with open(self.strings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier le format
        self.assertTrue(content.startswith('{\n\n\t"fleetInteractionDialog":{'))
        self.assertTrue('\t\t# Available tokens:' in content)
        self.assertTrue('\t\t"initialWithStationVsLargeFleet":' in content)
        
    def test_variables(self):
        """Teste la présence des variables système"""
        # Créer le fichier
        translate_strings()
        
        # Lire le contenu
        with open(self.strings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les variables
        variables = ['$faction', '$fleetName', '$firstName', '$lastName', 
                    '$fleetOrShip', '$repairedShipList', '$crewLost']
        for var in variables:
            self.assertIn(var, content)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=['dummy'])
    elif len(sys.argv) > 1:
        translate_strings(sys.argv[1])
    else:
        unittest.main()

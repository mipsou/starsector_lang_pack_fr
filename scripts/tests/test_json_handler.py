#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests unitaires pour le gestionnaire de fichiers JSON.
Vérifie le respect des conventions Starsector.
"""

import unittest
import json
import tempfile
import os
import sys
import shutil
from pathlib import Path

# Ajout du répertoire parent au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from handlers.json_handler import JsonHandler
from utils.logging_utils import setup_logger, LogConfig

class TestJsonHandler(unittest.TestCase):
    """Tests pour le gestionnaire de fichiers JSON."""
    
    def setUp(self):
        """Initialisation des tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_config = LogConfig(self.temp_dir)
        self.logger = setup_logger("test_json_handler", config=self.log_config)
        self.json_handler = JsonHandler(self.logger)
        
        # Création des fichiers de test
        self.tips_content = {
            "tips":[
                "Conseil simple",
                {"freq":2, "tip":"Conseil avec fréquence"}
            ]
        }
        
        self.tooltips_content = {
            "codex":{
                "section1":{
                    "title":"Titre",
                    "body":"Contenu"
                }
            },
            "combat":[
                "Conseil de combat"
            ]
        }
        
        self.strings_content = {
            "messages":{
                "greeting":"Bonjour $faction",
                "battle":"Le $fleetOrShip approche"
            }
        }
        
        # Crée les fichiers de test
        self.tips_file = Path(self.temp_dir) / "tips.json"
        self.tooltips_file = Path(self.temp_dir) / "tooltips.json"
        self.strings_file = Path(self.temp_dir) / "strings.json"
        
        self._write_json(self.tips_file, self.tips_content)
        self._write_json(self.tooltips_file, self.tooltips_content)
        self._write_json(self.strings_file, self.strings_content)
    
    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _write_json(self, file_path: Path, content: dict):
        """Écrit un contenu JSON dans un fichier."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)
    
    def test_format_validation(self):
        """Teste la validation du format JSON Starsector."""
        # Vérifie la structure tips.json
        result = self.json_handler.validate_format(self.tips_file)
        self.assertTrue(result.success)
        self.assertEqual(result.format_type, "tips")
        
        # Vérifie la structure tooltips.json
        result = self.json_handler.validate_format(self.tooltips_file)
        self.assertTrue(result.success)
        self.assertEqual(result.format_type, "tooltips")
        
        # Vérifie la structure strings.json
        result = self.json_handler.validate_format(self.strings_file)
        self.assertTrue(result.success)
        self.assertEqual(result.format_type, "strings")
    
    def test_quote_normalization(self):
        """Teste la normalisation des guillemets."""
        test_content = {
            "text": "Un « texte » avec 'guillemets' français"
        }
        test_file = Path(self.temp_dir) / "quotes.json"
        self._write_json(test_file, test_content)
        
        # Normalise les guillemets
        self.json_handler.fix_quotes(test_file)
        
        # Vérifie le résultat
        with open(test_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            self.assertEqual(content["text"], 'Un "texte" avec \'guillemets\' français')
    
    def test_indentation_format(self):
        """Teste le format d'indentation spécifique."""
        test_content = {"key":"value"}
        test_file = Path(self.temp_dir) / "indent.json"
        
        # Écrit avec l'indentation correcte
        self.json_handler.write_json(test_file, test_content)
        
        # Vérifie le format
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Vérifie l'indentation de 4 espaces
            self.assertIn('\n    "', content)
            # Vérifie pas d'espace après les deux points
            self.assertIn('":"', content)
            # Vérifie pas d'espace en fin de ligne
            self.assertNotIn(' \n', content)
    
    def test_utf8_encoding(self):
        """Teste l'encodage UTF-8 et les accents."""
        test_content = {
            "text": "Texte avec des accents : é à è ù"
        }
        test_file = Path(self.temp_dir) / "encoding.json"
        
        # Écrit le fichier
        self.json_handler.write_json(test_file, test_content)
        
        # Vérifie l'encodage
        with open(test_file, 'rb') as f:
            content = f.read()
            # Vérifie que c'est de l'UTF-8 valide
            content.decode('utf-8')
            # Vérifie la présence des accents
            self.assertIn('é'.encode('utf-8'), content)
    
    def test_structure_preservation(self):
        """Teste la préservation de la structure exacte."""
        # Charge un fichier original
        original = self.tips_content.copy()
        modified = {"tips": original["tips"].copy()}  # Copie profonde
        modified["tips"].append("Nouveau conseil")  # Ajoute un élément
        
        test_file = Path(self.temp_dir) / "structure.json"
        self._write_json(test_file, modified)
        
        # Vérifie la structure contre l'original
        result = self.json_handler.validate_against_original(test_file, original)
        self.assertTrue(result.valid_structure)  # La structure de base est valide
        self.assertFalse(result.identical)  # Mais le contenu est différent
        self.assertTrue(any("Longueur différente" in diff for diff in result.differences))

    def test_variable_preservation(self):
        """Teste la préservation des variables système."""
        test_content = {
            "message": "Le $faction envoie son $fleetOrShip"
        }
        test_file = Path(self.temp_dir) / "variables.json"
        self._write_json(test_file, test_content)
        
        # Vérifie les variables
        result = self.json_handler.validate_variables(test_file)
        self.assertTrue(result.success)
        self.assertEqual(len(result.variables), 2)
        self.assertIn("$faction", result.variables)
        self.assertIn("$fleetOrShip", result.variables)

    def test_escaped_quotes(self):
        """Teste la préservation des guillemets échappés."""
        test_content = {
            "text": 'Un texte avec des guillemets \\"test\\" et des «guillemets» français'
        }
        test_file = Path(self.temp_dir) / "escaped_quotes.json"
        self._write_json(test_file, test_content)
        
        # Normalise les guillemets
        self.json_handler.fix_quotes(test_file)
        
        # Vérifie le résultat
        with open(test_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            self.assertEqual(content["text"], 'Un texte avec des guillemets \\"test\\" et des "guillemets" français')

if __name__ == '__main__':
    unittest.main()

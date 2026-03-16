#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests d'intégration système pour la validation des traductions.
Vérifie l'interaction entre les différents composants.
"""

import unittest
import os
import shutil
import tempfile
import json
from pathlib import Path
import sys
import logging

# Ajout du répertoire parent au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from utils.path_utils import PathManager
from utils.format_utils import FormatUtils
from utils.binary_utils import find_control_chars_binary
from handlers.json_handler import JsonHandler
from handlers.mission_handler import MissionHandler

class TestSystemIntegration(unittest.TestCase):
    """Tests d'intégration système."""
    
    def setUp(self):
        """Initialisation des tests d'intégration."""
        # Configuration du logger
        self.logger = logging.getLogger('test_integration')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Configuration des chemins
        self.test_dir = Path(tempfile.mkdtemp())
        self.path_manager = PathManager(self.test_dir)
        
        # Configuration des chemins
        self.localization_dir = self.test_dir / 'localization'
        self.data_dir = self.localization_dir / 'data'
        self.strings_dir = self.data_dir / 'strings'
        self.missions_dir = self.data_dir / 'missions'
        
        # Création des répertoires de test
        os.makedirs(self.strings_dir)
        os.makedirs(self.missions_dir)
        
        # Initialisation des handlers
        self.json_handler = JsonHandler(self.logger)
        self.mission_handler = MissionHandler()
        
    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.test_dir)
    
    def test_complete_validation_workflow(self):
        """Test du workflow complet de validation."""
        # Création d'un fichier JSON de test
        json_file = self.strings_dir / 'test.json'
        json_content = {
            "tips": [
                {"freq":0, "tip":"Test avec fréquence"},
                "Test simple"
            ]
        }
        json_str = json.dumps(json_content, ensure_ascii=False, indent=4)
        json_str = FormatUtils.normalize_newlines(json_str)
        
        with open(json_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json_str)
        
        # Validation du fichier JSON
        result = self.json_handler.validate_format(json_file)
        self.assertTrue(result.success)
        
        # Test des caractères de contrôle
        control_chars = find_control_chars_binary(json_file)
        self.assertEqual(len(control_chars), 0, 
                        f"Caractères de contrôle trouvés aux positions : {[f'pos {pos}: {char}' for pos, char in control_chars]}")
        
        # Création d'un fichier mission de test
        mission_file = self.missions_dir / 'test_mission.txt'
        mission_content = """Lieu : Test
Date : 3014
Objectifs : Test des objectifs
Description : Test de la description"""
        
        with open(mission_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(mission_content)
        
        # Validation du fichier mission
        result = self.mission_handler.validate_file(mission_file)
        self.assertTrue(result.success)
    
    def test_error_handling(self):
        """Test de la gestion des erreurs."""
        # Test avec un fichier JSON invalide
        json_file = self.strings_dir / 'invalid.json'
        with open(json_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('{"invalid": [}')
        
        result = self.json_handler.validate_format(json_file)
        self.assertFalse(result.success)
        self.assertTrue('JSON invalide' in result.message or 'Expecting value' in result.message,
                       f"Message d'erreur inattendu : {result.message}")
        
        # Test avec un fichier mission invalide
        mission_file = self.missions_dir / 'invalid_mission.txt'
        with open(mission_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('Contenu invalide sans structure')
        
        result = self.mission_handler.validate_file(mission_file)
        self.assertFalse(result.success)
        self.assertIn('Structure invalide', result.message)

if __name__ == '__main__':
    unittest.main(verbosity=2)

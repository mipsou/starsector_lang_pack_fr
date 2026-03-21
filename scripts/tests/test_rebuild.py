"""Tests pour le gestionnaire de reconstruction."""

import sys
import unittest
from pathlib import Path
import tempfile
import shutil
import logging

# Ajoute le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from handlers.json.handler import JsonHandler

# Initialisation du handler JSON
logger = logging.getLogger(__name__)
json_handler = JsonHandler(logger)

class TestRebuildManager(unittest.TestCase):
    """Tests pour le gestionnaire de reconstruction."""
    
    def setUp(self):
        """Initialise l'environnement de test."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.json"
        self.test_data = {
            "key1": "value1",
            "key2": ["item1", "item2"],
            "key3": {"subkey": "subvalue"}
        }
    
    def test_format_detection(self):
        """Teste la détection du format JSON."""
        # Écrit le fichier JSON avec le handler
        success = json_handler.dump(self.test_data, self.test_file, starsector_format=True)
        self.assertTrue(success)
            
        # Vérifie que le fichier est valide
        result = json_handler.validate_format(self.test_file)
        self.assertTrue(result.is_valid)
    
    def test_format_preservation(self):
        """Teste la préservation du format lors de la reconstruction."""
        # Écrit le fichier original
        success = json_handler.dump(self.test_data, self.test_file, starsector_format=True)
        self.assertTrue(success)
        
        # Lit le contenu original
        with open(self.test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
            
        # Charge et réécrit le fichier
        data = json_handler.load(self.test_file)
        success = json_handler.dump(data, self.test_file, starsector_format=True)
        self.assertTrue(success)
        
        # Vérifie que le format est préservé
        with open(self.test_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        self.assertEqual(original_content.strip(), new_content.strip())
    
    def test_rebuild_tips(self):
        """Teste la reconstruction d'un fichier tips.json."""
        tips_data = {
            "tips": [
                "tip1",
                "tip2",
                {"freq": 2, "tip": "tip3"}
            ]
        }
        
        # Écrit le fichier tips
        success = json_handler.dump(tips_data, self.test_file, starsector_format=True)
        self.assertTrue(success)
        
        # Vérifie le contenu
        data = json_handler.load(self.test_file)
        self.assertIsNotNone(data)
        self.assertIn("tips", data)
        self.assertEqual(len(data["tips"]), 3)
    
    def test_rebuild_all(self):
        """Teste la reconstruction de plusieurs fichiers."""
        # Crée plusieurs fichiers de test
        files = []
        for i in range(3):
            file_path = Path(self.temp_dir) / f"test{i}.json"
            success = json_handler.dump(self.test_data, file_path, starsector_format=True)
            self.assertTrue(success)
            files.append(file_path)
        
        # Vérifie que tous les fichiers sont valides
        success_count = 0
        for file_path in files:
            result = json_handler.validate_format(file_path)
            if result.is_valid:
                success_count += 1
        
        self.assertGreater(success_count, 0)
    
    def test_json_writer_integration(self):
        """Teste l'intégration avec JsonWriter."""
        test_content = {
            "strings": {
                "test_id": {
                    "text": "Test avec guillemets \"imbriqués\"",
                    "category": "misc"
                }
            }
        }
        
        # Écrit le fichier avec guillemets spéciaux
        success = json_handler.dump(test_content, self.test_file, starsector_format=True)
        self.assertTrue(success)
        
        # Vérifie la conversion des guillemets
        data = json_handler.load(self.test_file)
        self.assertIn("strings", data)
        self.assertIn("test_id", data["strings"])
        self.assertIn("text", data["strings"]["test_id"])
        self.assertIn("«", data["strings"]["test_id"]["text"])
        self.assertIn("»", data["strings"]["test_id"]["text"])
    
    def test_json_writer_validation(self):
        """Teste la validation lors de l'écriture."""
        # Test avec des données valides
        test_content = {"valid": "content"}
        success = json_handler.dump(test_content, self.test_file, starsector_format=True)
        self.assertTrue(success)
        
        # Test avec des données invalides
        invalid_content = None
        success = json_handler.dump(invalid_content, self.test_file, starsector_format=True)
        self.assertFalse(success)
    
    def tearDown(self):
        """Nettoie l'environnement de test."""
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()

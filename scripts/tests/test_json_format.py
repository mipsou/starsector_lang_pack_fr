#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests pour le formatage JSON."""

import unittest
import logging
from pathlib import Path
import tempfile

from handlers.json.handler import JsonHandler
from handlers.starsector_json import FileType

# Initialisation du handler JSON
logger = logging.getLogger(__name__)
json_handler = JsonHandler(logger)

class TestJsonFormat(unittest.TestCase):
    """Tests pour le formatage JSON Starsector."""
    
    def setUp(self):
        """Initialise les données de test."""
        self.test_data = {
            "key1": "value1",
            "key2": ["item1", "item2"],
            "key3": {"subkey": "subvalue"}
        }
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.json"
    
    def test_parse_invalid_json(self):
        """Teste le parsing d'un JSON invalide."""
        invalid_json = "{invalid:json}"
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(invalid_json)
        result = json_handler.load(self.test_file)
        self.assertIsNone(result)
    
    def test_parse_valid_json(self):
        """Teste le parsing d'un JSON valide."""
        valid_json = '{"key": "value"}'
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(valid_json)
        result = json_handler.load(self.test_file)
        self.assertEqual(result, {"key": "value"})
    
    def test_format_strings_json(self):
        """Teste le formatage d'un fichier strings.json."""
        result = json_handler.dump(self.test_data, self.test_file, starsector_format=True)
        self.assertTrue(result)
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('"key1"', content)
        self.assertIn('"value1"', content)
    
    def test_format_invalid_data(self):
        """Teste le formatage de données invalides."""
        invalid_data = None
        result = json_handler.dump(invalid_data, self.test_file, starsector_format=True)
        self.assertFalse(result)
    
    def tearDown(self):
        """Nettoie les fichiers temporaires."""
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()

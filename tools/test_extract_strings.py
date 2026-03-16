#!/usr/bin/env python3
"""
Tests unitaires pour le script d'extraction des chaînes de caractères.
"""

import unittest
import os
import json
import csv
from pathlib import Path
import tempfile
import shutil
from extract_strings import detect_encoding, extract_csv, extract_json

class TestExtractStrings(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        
        # Création d'un fichier CSV de test
        self.test_csv = os.path.join(self.test_dir, "test.csv")
        with open(self.test_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text"])
            writer.writerow(["test_id", "Test text"])
            writer.writerow(["test_id2", "Test text 2"])

        # Création d'un fichier JSON de test
        self.test_json = os.path.join(self.test_dir, "test.json")
        test_data = {
            "key1": "value1",
            "key2": "value2"
        }
        with open(self.test_json, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)

    def test_detect_encoding(self):
        """Test de la détection d'encodage."""
        encoding = detect_encoding(self.test_csv)
        self.assertIn(encoding, ['utf-8', 'utf-8-sig'])

    def test_extract_csv(self):
        """Test de l'extraction CSV."""
        output_csv = os.path.join(self.test_dir, "output.csv")
        extract_csv(self.test_csv, output_csv)
        
        # Vérification du fichier de sortie
        self.assertTrue(os.path.exists(output_csv))
        with open(output_csv, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertTrue(rows[0]["text"].startswith("# "))

    def test_extract_json(self):
        """Test de l'extraction JSON."""
        output_json = os.path.join(self.test_dir, "output.json")
        extract_json(self.test_json, output_json)
        
        # Vérification du fichier de sortie
        self.assertTrue(os.path.exists(output_json))
        with open(output_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("# key1", data)
            self.assertIn("key1", data)
            self.assertEqual(data["# key1"], "value1")
            self.assertEqual(data["key1"], "")

if __name__ == "__main__":
    unittest.main()

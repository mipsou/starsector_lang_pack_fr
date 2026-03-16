#!/usr/bin/env python3
"""
Tests unitaires pour le convertisseur CSV vers JSON.
"""

import unittest
import os
import json
import csv
import tempfile
import shutil
from pathlib import Path
from convert_csv_to_json import CSVToJSONConverter

class TestCSVToJSONConverter(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        
        # Création d'un fichier CSV de test simple
        self.test_csv = os.path.join(self.test_dir, "test.csv")
        with open(self.test_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text"])
            writer.writerow(["key1", "value1"])
            writer.writerow(["key2", "value2"])
        
        # Création d'un fichier CSV de test complexe
        self.complex_csv = os.path.join(self.test_dir, "complex.csv")
        with open(self.complex_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text", "description"])
            writer.writerow(["key1", "value1", "desc1"])
            writer.writerow(["key2", "value2", "desc2"])
        
        # Fichiers de sortie
        self.output_json = os.path.join(self.test_dir, "output.json")
        self.complex_output = os.path.join(self.test_dir, "complex_output.json")
    
    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)
    
    def test_simple_conversion(self):
        """Test de conversion d'un CSV simple."""
        converter = CSVToJSONConverter(self.test_csv, self.output_json)
        success = converter.convert()
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.output_json))
        
        with open(self.output_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["key1"], "value1")
            self.assertEqual(data["key2"], "value2")
    
    def test_complex_conversion(self):
        """Test de conversion d'un CSV avec plusieurs colonnes."""
        converter = CSVToJSONConverter(self.complex_csv, self.complex_output)
        success = converter.convert()
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.complex_output))
        
        with open(self.complex_output, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["key1"]["text"], "value1")
            self.assertEqual(data["key1"]["description"], "desc1")
            self.assertEqual(data["key2"]["text"], "value2")
            self.assertEqual(data["key2"]["description"], "desc2")
    
    def test_error_handling(self):
        """Test de la gestion des erreurs."""
        # Test avec un fichier inexistant
        converter = CSVToJSONConverter(
            "fichier_inexistant.csv",
            self.output_json
        )
        success = converter.convert()
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()

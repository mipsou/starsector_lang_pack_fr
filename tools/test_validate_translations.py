#!/usr/bin/env python3
"""
Tests unitaires pour le validateur de traductions.
"""

import unittest
import os
import json
import csv
from pathlib import Path
import tempfile
import shutil
from validate_translations import TranslationValidator

class TestTranslationValidator(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        
        # Création d'un fichier CSV de test valide
        self.valid_csv = os.path.join(self.test_dir, "valid.csv")
        with open(self.valid_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text"])
            writer.writerow(["test_id", "Texte de test"])
            writer.writerow(["test_id2", "Un autre texte"])

        # Création d'un fichier CSV de test invalide
        self.invalid_csv = os.path.join(self.test_dir, "invalid.csv")
        with open(self.invalid_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id"])  # Colonne manquante
            writer.writerow(["test_id"])

        # Création d'un fichier JSON de test valide
        self.valid_json = os.path.join(self.test_dir, "valid.json")
        valid_data = {
            "key1": "valeur1",
            "key2": "valeur2"
        }
        with open(self.valid_json, "w", encoding="utf-8") as f:
            json.dump(valid_data, f, ensure_ascii=False, indent=2)

        # Création d'un fichier JSON de test avec avertissements
        self.warning_json = os.path.join(self.test_dir, "warning.json")
        warning_data = {
            "key1": "valeur  avec  espaces  multiples",
            "key2": "texte avec < html >"
        }
        with open(self.warning_json, "w", encoding="utf-8") as f:
            json.dump(warning_data, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)

    def test_validate_valid_csv(self):
        """Test de validation d'un CSV valide."""
        validator = TranslationValidator(self.test_dir)
        success, errors, warnings = validator.validate_all()
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)

    def test_validate_invalid_csv(self):
        """Test de validation d'un CSV invalide."""
        # Créer un dossier temporaire ne contenant que le fichier invalide
        invalid_dir = os.path.join(self.test_dir, "invalid")
        os.makedirs(invalid_dir)
        shutil.copy(self.invalid_csv, os.path.join(invalid_dir, "invalid.csv"))
        
        validator = TranslationValidator(invalid_dir)
        success, errors, warnings = validator.validate_all()
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)

    def test_validate_warnings(self):
        """Test de validation avec avertissements."""
        # Créer un dossier temporaire ne contenant que le fichier avec avertissements
        warning_dir = os.path.join(self.test_dir, "warning")
        os.makedirs(warning_dir)
        shutil.copy(self.warning_json, os.path.join(warning_dir, "warning.json"))
        
        validator = TranslationValidator(warning_dir)
        success, errors, warnings = validator.validate_all()
        self.assertTrue(success)  # Les avertissements ne causent pas d'échec
        self.assertEqual(len(errors), 0)
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("espaces multiples" in w for w in warnings))
        self.assertTrue(any("HTML" in w for w in warnings))

if __name__ == "__main__":
    unittest.main()

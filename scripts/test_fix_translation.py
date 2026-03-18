#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests unitaires pour le script de correction des traductions.

Auteur: Mipsou
Date: 2025-01-31
"""

import unittest
import json
import os
from pathlib import Path
import shutil
from fix_translation import fix_special_chars, validate_json_structure, remove_comments

class TestFixTranslation(unittest.TestCase):
    """Tests pour les fonctions de correction."""

    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = Path('test_data')
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_fix_special_chars(self):
        """Test de la correction des caractères spéciaux."""
        test_cases = [
            ('ééé', 'é'),
            ('ééà', 'à'),
            ('ééâ', 'â'),
            ('texte avec ééé', 'texte avec é')
        ]
        for input_text, expected in test_cases:
            self.assertEqual(fix_special_chars(input_text), expected)

    def test_validate_json_structure(self):
        """Test de la validation de structure JSON."""
        valid_json = '{"key": "value"}'
        invalid_json = '{"key": value"}'  # Guillemet manquant

        is_valid, _ = validate_json_structure(valid_json)
        self.assertTrue(is_valid)

        is_valid, error = validate_json_structure(invalid_json)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_remove_comments(self):
        """Test de la suppression des commentaires."""
        content = '''# Commentaire
        {"key": "value"} # Autre commentaire
        # Encore un commentaire
        "text"'''
        expected = '{"key": "value"}\n"text"'
        self.assertEqual(remove_comments(content).strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()

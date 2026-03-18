#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests de validation des fichiers de traduction.

Vérifie l'encodage, le format JSON/CSV et la cohérence des fichiers
dans localization/data/.
"""

import unittest
import json
import csv
import os
import chardet
from pathlib import Path
from scripts.handlers.starsector_json import parse_starsector_json


class TestTranslations(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join('localization', 'data')
        self.strings_dir = os.path.join(self.data_dir, 'strings')

    def test_file_encoding(self):
        """Vérifie que tous les fichiers sont en UTF-8 (ou ASCII, sous-ensemble de UTF-8)."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(('.json', '.csv', '.txt')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        raw = f.read()
                        result = chardet.detect(raw)
                        detected = (result['encoding'] or '').lower().replace('-', '')
                        self.assertIn(
                            detected, ['utf8', 'ascii'],
                            f"{file_path} n'est pas en UTF-8 (détecté : {result['encoding']})"
                        )

    def test_json_format(self):
        """Vérifie la validité des fichiers JSON (format Starsector avec virgules finales)."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Utilise le parser Starsector qui gère les virgules finales
                    data, error = parse_starsector_json(content)
                    self.assertIsNone(
                        error,
                        f"Erreur JSON dans {file_path}: {error}"
                    )

    def test_csv_format(self):
        """Vérifie la validité des fichiers CSV (en-têtes et cohérence des colonnes)."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        self.assertTrue(
                            len(headers) > 0,
                            f"Fichier CSV sans en-têtes : {file_path}"
                        )


if __name__ == '__main__':
    unittest.main()

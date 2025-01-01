#!/usr/bin/env python3
import unittest
import json
import csv
import os
import chardet

class TestTranslations(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join('data')
        self.config_dir = os.path.join(self.data_dir, 'config')
        self.strings_dir = os.path.join(self.data_dir, 'strings')

    def test_file_encoding(self):
        """Vérifie que tous les fichiers sont en UTF-8."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(('.json', '.csv')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        raw = f.read()
                        result = chardet.detect(raw)
                        self.assertEqual(result['encoding'].lower(), 'utf-8',
                                      f"{file_path} n'est pas en UTF-8")

    def test_json_format(self):
        """Vérifie la validité des fichiers JSON."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError as e:
                            self.fail(f"Erreur JSON dans {file_path}: {str(e)}")

    def test_csv_format(self):
        """Vérifie la validité des fichiers CSV."""
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        for row in reader:
                            self.assertEqual(len(row), len(headers),
                                          f"Nombre de colonnes incorrect dans {file_path}")

if __name__ == '__main__':
    unittest.main()

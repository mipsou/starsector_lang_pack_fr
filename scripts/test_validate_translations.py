#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import tempfile
import json
from pathlib import Path
from validate_translations import (
    TranslationConfig,
    MissionValidator,
    check_encoding,
    validate_json,
    validate_csv,
    compare_with_original
)

class TestValidateTranslations(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.config = TranslationConfig()
        
        # Redirection des chemins pour les tests
        self.config.base_dir = self.test_dir
        self.config.localization_dir = self.test_dir / 'localization'
        self.config.data_dir = self.config.localization_dir / 'data'
        self.config.strings_dir = self.config.data_dir / 'strings'
        self.config.missions_dir = self.config.data_dir / 'missions'
        
        # Création des répertoires de test
        self.config.strings_dir.mkdir(parents=True)
        self.config.missions_dir.mkdir(parents=True)
        
    def create_test_file(self, content, filename, encoding='utf-8'):
        """Crée un fichier de test avec le contenu spécifié."""
        file_path = self.test_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if isinstance(content, str):
            file_path.write_text(content, encoding=encoding)
        elif isinstance(content, dict):
            file_path.write_text(json.dumps(content, indent=2), encoding=encoding)
            
        return file_path
    
    def test_encoding_validation(self):
        """Test de la validation de l'encodage."""
        # Test UTF-8
        content = "Test content with UTF-8 é à ù"
        file_path = self.create_test_file(content, "test_utf8.txt", "utf-8")
        self.assertTrue(check_encoding(file_path))
        
        # Test autre encodage
        file_path = self.create_test_file(content, "test_latin1.txt", "latin1")
        self.assertFalse(check_encoding(file_path))
    
    def test_json_validation(self):
        """Test de la validation JSON."""
        # JSON valide
        content = {"key": "value", "nested": {"key": "value"}}
        file_path = self.create_test_file(content, "test.json")
        self.assertTrue(validate_json(file_path))
        
        # JSON invalide
        content = "{'key': 'value'"  # JSON mal formaté
        file_path = self.create_test_file(content, "invalid.json")
        self.assertFalse(validate_json(file_path))
    
    def test_csv_validation(self):
        """Test de la validation CSV."""
        # CSV valide
        content = "header1,header2\nvalue1,value2\nvalue3,value4"
        file_path = self.create_test_file(content, "test.csv")
        self.assertTrue(validate_csv(file_path))
        
        # CSV invalide (colonnes incohérentes)
        content = "header1,header2\nvalue1\nvalue3,value4"
        file_path = self.create_test_file(content, "invalid.csv")
        self.assertFalse(validate_csv(file_path))
    
    def test_mission_validation(self):
        """Test de la validation des missions."""
        validator = MissionValidator(self.config)
        
        # Mission valide
        content = "Lieu : Test\n"
        content += "Date : 3014\n"
        content += "Objectifs : Test\n"
        content += "Description : Un test avec la typographie française : parfait !\n"
        file_path = self.create_test_file(content, "missions/test/mission_text.txt")
        issues = validator.validate_mission_text(file_path)
        self.assertEqual(len(issues), 0, "La mission valide ne devrait pas avoir d'erreurs")
        
        # Mission avec erreurs typographiques
        content = "Lieu : Test\n"
        content += "Date : 3014\n"
        content += "Objectifs: Test sans espace\n"
        content += "Description: Test avec \"guillemets\" et points...\n"
        file_path = self.create_test_file(content, "missions/invalid/mission_text.txt")
        issues = validator.validate_mission_text(file_path)
        self.assertTrue(len(issues) > 0, "Devrait détecter les erreurs typographiques")
    
    def test_compare_with_original(self):
        """Test de la comparaison avec les fichiers originaux."""
        # Fichiers identiques
        orig_content = {"key1": "value1", "key2": {"nested": "value2"}}
        translated_content = {"key1": "valeur1", "key2": {"nested": "valeur2"}}
        
        orig_file = self.create_test_file(orig_content, "original/test.json")
        translated_file = self.create_test_file(translated_content, "localization/test.json")
        
        self.assertTrue(compare_with_original(translated_file, orig_file))
        
        # Fichiers différents
        translated_content = {"key1": "valeur1", "extra": "value"}
        translated_file = self.create_test_file(translated_content, "localization/different.json")
        
        self.assertFalse(compare_with_original(translated_file, orig_file))
    
    def tearDown(self):
        """Nettoyage après les tests."""
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()

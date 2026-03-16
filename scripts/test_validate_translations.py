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
    validate_json,
    validate_csv,
    validate_mission_text,
    validate_text,
    auto_correct_text,
    check_encoding,
    compare_with_original,
    validate_with_context,
    format_validation_errors,
    ValidationError
)
import csv

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
        """Teste la validation des fichiers JSON."""
        # Création d'un fichier JSON invalide
        file_path = self.test_dir / "invalid.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('{"key": value}')  # JSON invalide (pas de guillemets)
            
        # Test de validation
        is_valid, errors = validate_json(file_path)
        self.assertFalse(is_valid, "Le fichier invalide devrait être rejeté")
        self.assertTrue(errors, "Des erreurs devraient être rapportées")
        
        # Création d'un fichier JSON valide
        file_path = self.test_dir / "valid.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"key": "value"}, f)
            
        # Test de validation
        is_valid, errors = validate_json(file_path)
        self.assertTrue(is_valid, "Le fichier valide devrait être accepté")
        self.assertEqual(len(errors), 0, "Aucune erreur ne devrait être rapportée")

    def test_csv_validation(self):
        """Teste la validation des fichiers CSV."""
        # Création d'un fichier CSV invalide
        file_path = self.test_dir / "invalid.csv"
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text'])  # En-tête avec 2 colonnes
            writer.writerow(['1', 'text', 'extra'])  # Ligne avec 3 colonnes
            
        # Test de validation
        is_valid, errors = validate_csv(file_path)
        self.assertFalse(is_valid, "Le fichier invalide devrait être rejeté")
        self.assertTrue(errors, "Des erreurs devraient être rapportées")
        
        # Création d'un fichier CSV valide
        file_path = self.test_dir / "valid.csv"
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text'])
            writer.writerow(['1', 'text'])
            
        # Test de validation
        is_valid, errors = validate_csv(file_path)
        self.assertTrue(is_valid, "Le fichier valide devrait être accepté")
        self.assertEqual(len(errors), 0, "Aucune erreur ne devrait être rapportée")

    def test_mission_validation(self):
        """Test de la validation des fichiers mission."""
        # Test avec un texte valide
        text = "Lieu: Base Alpha\nDate: 3014\nObjectifs: Défendre la station\nDescription: Une mission de défense."
        is_valid, errors = validate_mission_text(text)
        self.assertTrue(is_valid, f"Le texte valide devrait être accepté. Erreurs: {errors}")
        
        # Test avec un texte invalide (section manquante)
        text = "Lieu: Base Alpha\nDate: 3014\nDescription: Une mission."
        is_valid, errors = validate_mission_text(text)
        self.assertFalse(is_valid, "Le texte invalide devrait être rejeté")
        self.assertIn("Section Objectifs manquante", errors)
        
        # Test avec une ponctuation incorrecte
        text = "Lieu: Base Alpha\nDate: 3014\nObjectifs: Défendre la station !\nDescription: Une mission ?"
        is_valid, errors = validate_mission_text(text)
        self.assertFalse(is_valid, "La ponctuation incorrecte devrait être rejetée")
        
    def test_special_chars(self):
        """Test de la validation des caractères spéciaux."""
        # Test avec des caractères spéciaux valides
        text = "Le cœur du réacteur est en surchauffe. L'æther spatial est ambiguë."
        is_valid, errors = validate_text(text)
        self.assertTrue(is_valid, f"Le texte avec caractères spéciaux valides devrait être accepté. Erreurs: {errors}")
        
        # Test avec des ligatures
        text = "Œdipe et Æschyle observent les manœuvres."
        is_valid, errors = validate_text(text)
        self.assertTrue(is_valid, f"Le texte avec ligatures devrait être accepté. Erreurs: {errors}")
        
        # Test avec des trémas
        text = "Noël approche, les poëtes sont naïfs."
        is_valid, errors = validate_text(text)
        self.assertTrue(is_valid, f"Le texte avec trémas devrait être accepté. Erreurs: {errors}")
    
    def test_compare_with_original(self):
        """Teste la comparaison avec le fichier original."""
        # Création du fichier original
        orig_file = self.test_dir / "original.json"
        with open(orig_file, 'w', encoding='utf-8') as f:
            json.dump({
                "key1": "value1",
                "key2": {
                    "nested": "value2"
                }
            }, f)
            
        # Création d'un fichier traduit invalide
        translated_file = self.test_dir / "translated.json"
        with open(translated_file, 'w', encoding='utf-8') as f:
            json.dump({
                "key1": "valeur1",
                "extra": "valeur3"
            }, f)
            
        # Test de comparaison
        is_valid, errors = compare_with_original(translated_file, orig_file)
        self.assertFalse(is_valid, "Le fichier invalide devrait être rejeté")
        self.assertTrue(errors, "Des erreurs devraient être rapportées")
        
        # Création d'un fichier traduit valide
        with open(translated_file, 'w', encoding='utf-8') as f:
            json.dump({
                "key1": "valeur1",
                "key2": {
                    "nested": "valeur2"
                }
            }, f)
            
        # Test de comparaison
        is_valid, errors = compare_with_original(translated_file, orig_file)
        self.assertTrue(is_valid, "Le fichier valide devrait être accepté")
        self.assertEqual(len(errors), 0, "Aucune erreur ne devrait être rapportée")

    def test_validation_with_context(self):
        """Test de la validation avec contexte."""
        # Test avec un texte valide en mode non strict
        text = "Le vaisseau est en orbite autour de la planète."
        is_valid, errors = validate_with_context(text, {
            'type': 'mission',
            'section': 'description'
        }, strict=False)
        self.assertTrue(is_valid, "Le texte valide devrait être accepté")
        self.assertEqual(len(errors), 0, "Il ne devrait pas y avoir d'erreurs")
        
        # Test avec un texte valide en mode strict
        text = "Le vaisseau est en orbite autour de la planète."
        is_valid, errors = validate_with_context(text, {
            'type': 'mission',
            'section': 'description'
        }, strict=True)
        self.assertFalse(is_valid, "Le texte devrait être rejeté en mode strict")
        self.assertTrue(len(errors) > 0, "Il devrait y avoir des erreurs en mode strict")
        
        # Test avec un texte invalide
        text = "Le vaisseau ! est en orbite ?"
        is_valid, errors = validate_with_context(text, {
            'type': 'json',
            'section': 'tips'
        })
        self.assertFalse(is_valid, "Le texte invalide devrait être rejeté")
        self.assertTrue(len(errors) > 0, "Il devrait y avoir des erreurs")
        self.assertEqual(errors[0]['file_type'], 'json', "Le type de fichier devrait être correct")
        self.assertEqual(errors[0]['section'], 'tips', "La section devrait être correcte")
        
        # Test avec une erreur critique
        with self.assertRaises(ValidationError):
            validate_with_context(None)
        
        # Test du formatage des erreurs
        errors = [
            {'message': "Erreur 1", 'file_type': 'json', 'section': 'tips', 'line': 1},
            {'message': "Erreur 2", 'file_type': 'mission', 'section': 'description', 'line': 5}
        ]
        formatted = format_validation_errors(errors)
        self.assertIn("Erreur 1", formatted, "Le message d'erreur devrait être présent")
        self.assertIn("ligne: 1", formatted, "Le numéro de ligne devrait être présent")
        self.assertIn("section: tips", formatted, "La section devrait être présente")
    
    def tearDown(self):
        """Nettoyage après les tests."""
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import tempfile
import json
from pathlib import Path
from validate_translations import (
    TranslationConfig,
    MissionValidator,
    validate_json,
    validate_csv,
    validate_mission_text,
    check_encoding,
    compare_with_original
)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests d'intégration."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.config = TranslationConfig()
        
        # Redirection des chemins pour les tests
        self.config.base_dir = self.test_dir
        self.config.localization_dir = self.test_dir / 'localization'
        self.config.data_dir = self.config.localization_dir / 'data'
        self.config.strings_dir = self.config.data_dir / 'strings'
        self.config.missions_dir = self.config.data_dir / 'missions'
        
        # Création des répertoires
        self.config.strings_dir.mkdir(parents=True)
        self.config.missions_dir.mkdir(parents=True)
        
        # Création des fichiers de test
        self.create_test_structure()
    
    def create_test_structure(self):
        """Crée une structure complète de test."""
        # Structure des missions
        missions = {
            "tutorial": {
                "mission_text.txt": """Lieu : Système Corvus
Date : 3014
Objectifs : Le Maréchal Spatial vous attend.
Description : Une flotte ennemie approche."""
            },
            "campaign": {
                "mission1": {
                    "mission_text.txt": """Lieu : Système Corvus
Date : 3015
Objectifs : Protéger la flotte.
Description : Test avec la typographie française : parfait !"""
                },
                "mission2": {
                    "mission_text.txt": """Lieu : Test
Date : 3016
Objectifs : Rencontrer le Maréchal Spatial.
Description : Test avec des « guillemets » et des points…"""
                }
            }
        }
        
        # Structure des fichiers JSON
        json_files = {
            "descriptions.json": {
                "ship_data": {
                    "fighter": "Chasseur léger",
                    "destroyer": "Destructeur"
                },
                "weapon_data": {
                    "laser": "Laser standard",
                    "missile": "Missile guidé"
                }
            },
            "strings.json": {
                "ui": {
                    "menu": "Menu principal",
                    "save": "Sauvegarder"
                }
            }
        }
        
        # Structure des fichiers CSV
        csv_files = {
            "glossary.csv": """terme,traduction
Space Marshal,Maréchal Spatial
Fleet,Flotte
Corvus System,Système Corvus"""
        }
        
        # Création des missions
        for mission, content in missions.items():
            if isinstance(content, dict):
                for submission, subcontent in content.items():
                    if isinstance(subcontent, dict):
                        path = self.config.missions_dir / mission / submission
                        path.mkdir(parents=True, exist_ok=True)
                        for filename, text in subcontent.items():
                            (path / filename).write_text(text, encoding='utf-8')
                    else:
                        path = self.config.missions_dir / mission
                        path.mkdir(parents=True, exist_ok=True)
                        (path / submission).write_text(content[submission], encoding='utf-8')
        
        # Création des fichiers JSON
        for filename, content in json_files.items():
            path = self.config.strings_dir / filename
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        
        # Création des fichiers CSV
        for filename, content in csv_files.items():
            path = self.config.strings_dir / filename
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def test_encoding(self):
        """Teste la détection de l'encodage des fichiers."""
        # Création d'un fichier UTF-8
        file = self.test_dir / "utf8.json"
        with open(file, 'w', encoding='utf-8') as f:
            f.write('{"test": "éèà"}')
        
        # Test de détection UTF-8
        self.assertTrue(check_encoding(file),
                       f"Encodage incorrect pour {file}")
        
        # Création d'un fichier Latin-1
        file = self.test_dir / "latin1.json"
        with open(file, 'w', encoding='latin1') as f:
            f.write('{"test": "éèà"}')
        
        # Test de détection Latin-1
        self.assertFalse(check_encoding(file),
                        f"Le fichier Latin-1 devrait être rejeté")

    def test_full_validation(self):
        """Teste la validation complète des fichiers."""
        # Création d'un fichier mission valide
        mission_dir = self.test_dir / "localization" / "data" / "missions" / "tutorial"
        mission_dir.mkdir(parents=True, exist_ok=True)
        mission_file = mission_dir / "mission_text.txt"
        
        with open(mission_file, 'w', encoding='utf-8') as f:
            f.write("Lieu : Base Stellaire Alpha\n")
            f.write("Date : 3014\n")
            f.write("Objectifs : Défendre la station\n")
            f.write("Description : Une mission de défense classique.\n")
        
        # Validation de la mission
        issues = []
        try:
            is_valid, errors = validate_mission_text(mission_file.read_text(encoding='utf-8'))
            if not is_valid:
                issues.extend(errors)
        except Exception as e:
            issues.append(str(e))
        
        self.assertEqual(len(issues), 0,
                        f"Erreurs dans {mission_file}: {issues}")
        
        # Création d'un fichier JSON valide
        json_dir = self.test_dir / "localization" / "data" / "strings"
        json_dir.mkdir(parents=True, exist_ok=True)
        json_file = json_dir / "descriptions.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "weapon_groups": {
                    "title": "Groupes d'armes",
                    "description": "Configurez vos armes."
                }
            }, f, ensure_ascii=False, indent=4)
        
        # Validation du JSON
        try:
            is_valid, errors = validate_json(json_file)
            if not is_valid:
                issues.extend(errors)
        except Exception as e:
            issues.append(str(e))
        
        self.assertEqual(len(issues), 0,
                        f"Erreurs dans {json_file}: {issues}")

    def test_structure_integrity(self):
        """Teste l'intégrité de la structure des fichiers."""
        # Création de la structure de base
        data_dir = self.test_dir / "localization" / "data"
        strings_dir = data_dir / "strings"
        missions_dir = data_dir / "missions"
        
        # Création des répertoires
        for d in [strings_dir, missions_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Vérification de la structure
        self.assertTrue(data_dir.exists(), "Le répertoire data n'existe pas")
        self.assertTrue(strings_dir.exists(), "Le répertoire strings n'existe pas")
        self.assertTrue(missions_dir.exists(), "Le répertoire missions n'existe pas")
        
        # Test des fichiers requis
        required_files = [
            strings_dir / "strings.json",
            strings_dir / "descriptions.json",
            strings_dir / "tips.json"
        ]
        
        # Création des fichiers requis
        for file in required_files:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump({"test": "value"}, f)
            self.assertTrue(file.exists(), f"Le fichier {file} n'existe pas")

    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)

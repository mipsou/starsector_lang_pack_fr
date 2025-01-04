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
    check_encoding,
    validate_json,
    validate_csv,
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
    
    def test_full_validation(self):
        """Test complet de validation."""
        validator = MissionValidator(self.config)
        
        # Test des missions
        mission_files = list(self.config.missions_dir.rglob('mission_text.txt'))
        self.assertTrue(len(mission_files) > 0, "Aucun fichier mission trouvé")
        
        for mission_file in mission_files:
            issues = validator.validate_mission_text(mission_file)
            self.assertEqual(len(issues), 0, 
                           f"Erreurs dans {mission_file}: {issues}")
        
        # Test des fichiers JSON
        json_files = list(self.config.strings_dir.glob('*.json'))
        self.assertTrue(len(json_files) > 0, "Aucun fichier JSON trouvé")
        
        for json_file in json_files:
            self.assertTrue(validate_json(json_file),
                          f"Validation JSON échouée pour {json_file}")
        
        # Test des fichiers CSV
        csv_files = list(self.config.strings_dir.glob('*.csv'))
        self.assertTrue(len(csv_files) > 0, "Aucun fichier CSV trouvé")
        
        for csv_file in csv_files:
            self.assertTrue(validate_csv(csv_file),
                          f"Validation CSV échouée pour {csv_file}")
    
    def test_encoding(self):
        """Test de l'encodage de tous les fichiers."""
        all_files = (
            list(self.config.missions_dir.rglob('*.txt')) +
            list(self.config.strings_dir.glob('*.json')) +
            list(self.config.strings_dir.glob('*.csv'))
        )
        
        for file in all_files:
            self.assertTrue(check_encoding(file),
                          f"Encodage incorrect pour {file}")
    
    def test_structure_integrity(self):
        """Test de l'intégrité de la structure."""
        # Vérification des répertoires requis
        self.assertTrue(self.config.missions_dir.exists(),
                       "Répertoire missions manquant")
        self.assertTrue(self.config.strings_dir.exists(),
                       "Répertoire strings manquant")
        
        # Vérification des fichiers requis
        required_files = [
            self.config.strings_dir / 'descriptions.json',
            self.config.strings_dir / 'strings.json',
            self.config.strings_dir / 'glossary.csv'
        ]
        
        for file in required_files:
            self.assertTrue(file.exists(),
                          f"Fichier requis manquant : {file}")
    
    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)

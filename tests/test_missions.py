#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from pathlib import Path
import csv

class TestMissions:
    """Tests pour la validation des missions."""
    
    @pytest.fixture
    def missions_dir(self):
        """Fixture pour le répertoire des missions."""
        return Path('localization/fr/data/missions')
    
    @pytest.fixture
    def original_missions_dir(self):
        """Fixture pour le répertoire original des missions."""
        return Path('original/data/missions')
    
    def test_missions_dir_exists(self, missions_dir):
        """Vérifie que le répertoire des missions existe."""
        assert missions_dir.exists(), f"Le répertoire {missions_dir} n'existe pas"
        assert missions_dir.is_dir(), f"{missions_dir} n'est pas un répertoire"
    
    def test_all_missions_present(self, missions_dir, original_missions_dir):
        """Vérifie que toutes les missions sont présentes."""
        original_files = set(f.name for f in original_missions_dir.glob('*.json'))
        translated_files = set(f.name for f in missions_dir.glob('*.json'))
        
        missing_files = original_files - translated_files
        assert not missing_files, f"Missions manquantes: {missing_files}"
    
    def test_missions_valid_json(self, missions_dir):
        """Vérifie que tous les fichiers sont des JSON valides."""
        invalid_files = []
        for mission_file in missions_dir.glob('*.json'):
            try:
                with open(mission_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                invalid_files.append((mission_file.name, str(e)))
                
        assert not invalid_files, f"Fichiers JSON invalides: {invalid_files}"
    
    def test_missions_structure(self, missions_dir, original_missions_dir):
        """Vérifie la structure des missions."""
        structure_errors = []
        
        for mission_file in missions_dir.glob('*.json'):
            original_file = original_missions_dir / mission_file.name
            
            with open(mission_file, 'r', encoding='utf-8') as f:
                translated = json.load(f)
            with open(original_file, 'r', encoding='utf-8') as f:
                original = json.load(f)
                
            # Vérifie les clés de premier niveau
            if set(translated.keys()) != set(original.keys()):
                structure_errors.append(
                    (mission_file.name, "Clés de premier niveau différentes")
                )
                
            # Vérifie les étapes de mission
            if 'stages' in translated and 'stages' in original:
                if len(translated['stages']) != len(original['stages']):
                    structure_errors.append(
                        (mission_file.name, "Nombre d'étapes différent")
                    )
                    
        assert not structure_errors, f"Erreurs de structure: {structure_errors}"
    
    def test_missions_no_empty_translations(self, missions_dir):
        """Vérifie qu'il n'y a pas de traductions vides."""
        empty_translations = []
        
        for mission_file in missions_dir.glob('*.json'):
            with open(mission_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            def check_empty(obj, path):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, str) and not value.strip():
                            empty_translations.append((mission_file.name, f"{path}.{key}"))
                        elif isinstance(value, (dict, list)):
                            check_empty(value, f"{path}.{key}")
                elif isinstance(obj, list):
                    for i, value in enumerate(obj):
                        check_empty(value, f"{path}[{i}]")
                            
            check_empty(data, mission_file.name)
                
        assert not empty_translations, \
            f"Traductions vides trouvées: {empty_translations}"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from pathlib import Path

class TestTips:
    """Tests pour la validation des tips."""
    
    @pytest.fixture
    def tips_file(self):
        """Fixture pour le fichier de tips."""
        return Path('localization/fr/data/strings/tips.json')
    
    @pytest.fixture
    def original_tips(self):
        """Fixture pour les tips originaux."""
        return Path('original/data/strings/tips.json')
    
    def test_tips_file_exists(self, tips_file):
        """Vérifie que le fichier de tips existe."""
        assert tips_file.exists(), f"Le fichier {tips_file} n'existe pas"
    
    def test_tips_is_valid_json(self, tips_file):
        """Vérifie que le fichier est un JSON valide."""
        try:
            with open(tips_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Le fichier {tips_file} n'est pas un JSON valide: {str(e)}")
    
    def test_tips_structure_matches_original(self, tips_file, original_tips):
        """Vérifie que la structure correspond à l'original."""
        with open(tips_file, 'r', encoding='utf-8') as f:
            translated = json.load(f)
        with open(original_tips, 'r', encoding='utf-8') as f:
            original = json.load(f)
            
        assert set(translated.keys()) == set(original.keys()), \
            "Les clés ne correspondent pas à l'original"
    
    def test_tips_no_empty_translations(self, tips_file):
        """Vérifie qu'il n'y a pas de traductions vides."""
        with open(tips_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        empty_translations = []
        for key, value in data.items():
            if not value.strip():
                empty_translations.append(key)
                
        assert not empty_translations, \
            f"Traductions vides trouvées pour les clés: {empty_translations}"
    
    def test_tips_french_typography(self, tips_file):
        """Vérifie les règles typographiques françaises de base."""
        with open(tips_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        typography_errors = []
        for key, value in data.items():
            # Vérifie les espaces avant la ponctuation double
            if any(p + ' ' in value for p in ':;!?'):
                typography_errors.append((key, "Espace manquant avant ponctuation double"))
            # Vérifie les guillemets français
            if '"' in value:
                typography_errors.append((key, "Guillemets droits au lieu de guillemets français"))
                
        assert not typography_errors, \
            f"Erreurs typographiques trouvées: {typography_errors}"

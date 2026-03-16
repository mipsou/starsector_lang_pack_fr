#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'tools'))

from validate_json import validate_json, validate_starsector_json
from validate_translations import TranslationConfig, check_encoding, validate_csv, MissionValidator

# Force l'encodage en UTF-8 pour la sortie
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

@pytest.fixture
def config():
    return TranslationConfig()

@pytest.fixture
def mission_validator(config):
    return MissionValidator(config)

def test_check_encoding_valid():
    """Test de validation d'encodage UTF-8 valide."""
    test_file = "test_utf8.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Test de contenu UTF-8 « » é à")
    assert check_encoding(test_file) == True
    os.remove(test_file)

def test_check_encoding_invalid():
    """Test de validation d'encodage non-UTF-8."""
    test_file = "test_latin1.txt"
    with open(test_file, "w", encoding="latin-1") as f:
        f.write("Test de contenu Latin-1")
    assert check_encoding(test_file) == False
    os.remove(test_file)

def test_validate_json_valid():
    """Test de validation JSON valide."""
    test_file = "test_valid.json"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write('{"test": "value"}')
    assert validate_json(test_file) == True
    os.remove(test_file)

def test_validate_json_invalid():
    """Test de validation JSON invalide."""
    test_file = "test_invalid.json"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write('{"test": value}')  # JSON invalide
    assert validate_json(test_file) == False
    os.remove(test_file)

def test_validate_starsector_json():
    """Test de validation JSON au format Starsector."""
    test_file = "test_starsector.json"
    content = '''{
        "codex": {
            "test": {
                "title": "Test",
                "body": "Test description"
            }
        }
    }'''
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    assert validate_starsector_json(content) == True
    os.remove(test_file)

def test_validate_starsector_json_invalid():
    """Test de validation JSON au format Starsector invalide."""
    test_file = "test_starsector_invalid.json"
    content = '''{
        "invalid_section": {
            "test": "value"
        }
    }'''
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    assert validate_starsector_json(content) == False
    os.remove(test_file)

def test_validate_typography(mission_validator):
    """Test de validation typographique."""
    # Définition des caractères spéciaux
    GUILLEMET_OUVRANT = '\u00AB'  # «
    GUILLEMET_FERMANT = '\u00BB'  # »
    POINTS_SUSPENSION = '\u2026'   # …
    APOSTROPHE = '\u2019'         # '
    
    # Test des caractères valides
    valid_text = f"Test des guillemets {GUILLEMET_OUVRANT} français {GUILLEMET_FERMANT} et de l{APOSTROPHE}apostrophe{POINTS_SUSPENSION}"
    assert mission_validator.validate_typography(valid_text) == True
    
    # Test des caractères invalides
    invalid_text = 'Test with "English" quotes...'
    assert mission_validator.validate_typography(invalid_text) == False
    
    # Test des espaces typographiques
    spacing_text = f"Test des espaces;:!? et des guillemets{GUILLEMET_OUVRANT}mal{GUILLEMET_FERMANT}espacés"
    assert mission_validator.validate_typography(spacing_text) == False
    
    # Test des apostrophes
    apostrophe_text = "L'apostrophe droite n'est pas correcte"
    assert mission_validator.validate_typography(apostrophe_text) == False

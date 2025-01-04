#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

from validate_translations import TranslationConfig, check_encoding, validate_json, validate_csv, MissionValidator

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
        f.write("Test de contenu Latin-1 é à")
    assert check_encoding(test_file) == False
    os.remove(test_file)

def test_validate_json_valid():
    """Test de validation JSON valide."""
    test_file = "test_valid.json"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write('{"key": "value", "nested": {"key": "value"}}')
    assert validate_json(test_file) == True
    os.remove(test_file)

def test_validate_json_invalid():
    """Test de validation JSON invalide."""
    test_file = "test_invalid.json"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write('{"key": "value", "nested": {key": "value"}}')
    assert validate_json(test_file) == False
    os.remove(test_file)

def test_validate_typography(mission_validator):
    """Test de validation typographique."""
    valid_text = "Voici un texte « bien formaté » avec des points de suspension…"
    invalid_text = "Voici un texte 'mal formate' avec des points..."
    
    assert mission_validator.validate_typography(valid_text) == True
    assert mission_validator.validate_typography(invalid_text) == False

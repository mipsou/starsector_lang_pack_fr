#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

from update_translations import TranslationConfig, detect_encoding, clean_json_content

@pytest.fixture
def config():
    return TranslationConfig()

def test_detect_encoding_utf8():
    """Test de détection d'encodage UTF-8."""
    test_file = "test_utf8.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Test de contenu UTF-8 « » é à")
    assert detect_encoding(test_file).lower() in ['utf-8', 'utf8', 'ascii']
    os.remove(test_file)

def test_detect_encoding_latin1():
    """Test de détection d'encodage Latin-1."""
    test_file = "test_latin1.txt"
    with open(test_file, "w", encoding="latin-1") as f:
        f.write("Test de contenu Latin-1 é à")
    assert detect_encoding(test_file).lower() in ['iso-8859-1', 'latin-1']
    os.remove(test_file)

def test_clean_json_content():
    """Test de nettoyage de contenu JSON."""
    dirty_json = """
    {
        # Commentaire à supprimer
        "key1": "value1",
        "key2": "value2",    # Autre commentaire
        "array": [
            "item1",
            "item2",    # Commentaire
        ],
    }
    """
    clean_json = clean_json_content(dirty_json)
    assert "#" not in clean_json
    assert clean_json.count(",") == 2  # Deux virgules valides restantes
    assert clean_json.strip().endswith("}")  # Pas de virgule finale

def test_backup_naming(config):
    """Test du format de nommage des backups."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config.base_dir / f'localization.old/backup_{timestamp}'
    assert str(backup_path).endswith(timestamp)

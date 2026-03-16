#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# Import explicite depuis scripts/ (pas tools/)
from scripts.update_translations import TranslationConfig, detect_encoding, clean_json_content

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

def test_detect_encoding_non_utf8():
    """Test de détection d'encodage non-UTF-8."""
    test_file = "test_latin1.txt"
    with open(test_file, "w", encoding="latin-1") as f:
        f.write("Test de contenu Latin-1 \xe9 \xe0")
    detected = detect_encoding(test_file).lower()
    # chardet peut détecter comme iso-8859-1, latin-1, ou windows-1252/1255
    # L'important est que ce ne soit pas détecté comme utf-8
    assert detected not in ['utf-8', 'utf8', 'ascii'], (
        f"Le fichier Latin-1 ne devrait pas être détecté comme {detected}"
    )
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
    # Après nettoyage : "key1": "value1", | "key2": "value2", | "item1", = 3 virgules
    # (virgules finales avant ] et } supprimées, virgules entre éléments conservées)
    assert clean_json.count(",") == 3
    assert clean_json.strip().endswith("}")  # Pas de virgule finale

def test_backup_naming(config):
    """Test du format de nommage des backups."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config.base_dir / f'localization.old/backup_{timestamp}'
    assert str(backup_path).endswith(timestamp)

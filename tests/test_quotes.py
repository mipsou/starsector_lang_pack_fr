#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests de la conversion des guillemets.
Vérifie la conversion bidirectionnelle et les cas spéciaux.
"""

import pytest
from pathlib import Path
from tools.fix_quotes import fix_quotes

def test_to_french_quotes():
    """Test de la conversion vers les guillemets français."""
    # Les guillemets externes restent en anglais pour JSON
    text = 'Test avec "guillemets"'
    expected = 'Test avec "guillemets"'
    assert fix_quotes(text) == expected

    text = 'Test avec "plusieurs" "guillemets"'
    expected = 'Test avec "plusieurs" "guillemets"'
    assert fix_quotes(text) == expected

def test_nested_quotes():
    """Test des guillemets imbriqués."""
    # Niveau 0 : guillemets anglais (")
    # Niveau 1 : guillemets français (« »)
    # Niveau 2 : guillemets français niveau 2 (‹ ›)
    text = 'Test avec "citation et "sous-citation" imbriquée"'
    expected = 'Test avec "citation et « sous-citation » imbriquée"'
    assert fix_quotes(text) == expected

    text = '"Citation 1" avec "citation 2 et "sous-citation" imbriquée"'
    expected = '"Citation 1" avec "citation 2 et « sous-citation » imbriquée"'
    assert fix_quotes(text) == expected

def test_preserve_escaped_quotes():
    """Test de la préservation des guillemets échappés."""
    text = 'Test avec \\"guillemets\\" échappés'
    expected = 'Test avec \\"guillemets\\" échappés'
    assert fix_quotes(text) == expected

if __name__ == "__main__":
    pytest.main([__file__])

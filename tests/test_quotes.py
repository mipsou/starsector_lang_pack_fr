#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests de la conversion des guillemets.
Vérifie la conversion bidirectionnelle et les cas spéciaux.

La fonction fix_quotes (via convert_quotes_starsector) convertit :
- Niveau 0 : guillemets droits -> guillemets français doubles (« ... »)
- Niveau 1+ : guillemets droits -> guillemets français simples (< ... >)
- Utilise l'espace fine insécable (\u202f) autour des guillemets
"""

import pytest
from pathlib import Path
from tools.fix_quotes import fix_quotes

# Espace fine insécable utilisé par le convertisseur
NNBSP = '\u202f'


def test_to_french_quotes():
    """Test de la conversion vers les guillemets français."""
    text = 'Test avec "guillemets"'
    expected = f'Test avec \xab{NNBSP}guillemets{NNBSP}\xbb'
    assert fix_quotes(text) == expected

    text = 'Test avec "plusieurs" "guillemets"'
    result = fix_quotes(text)
    assert f'\xab{NNBSP}' in result, "Doit contenir des guillemets ouvrants français"
    assert f'{NNBSP}\xbb' in result, "Doit contenir des guillemets fermants français"


def test_nested_quotes():
    """Test des guillemets imbriqués."""
    # Niveau 0 : guillemets français doubles (« »)
    # Niveau 1 : guillemets français simples (< >)
    text = 'Test avec "citation et "sous-citation" imbriquée"'
    result = fix_quotes(text)
    assert f'\xab{NNBSP}' in result, "Doit contenir des guillemets ouvrants niveau 0"
    assert f'\u2039{NNBSP}' in result, "Doit contenir des guillemets ouvrants niveau 1"


def test_no_quotes():
    """Test qu'un texte sans guillemets n'est pas modifié."""
    text = "Pas de guillemets ici"
    assert fix_quotes(text) == text


def test_structures_preserved():
    """Test que les structures JSON/Starsector ne sont pas modifiées."""
    text = '{"key": "value"}'
    assert fix_quotes(text) == text, "Les structures JSON doivent être préservées"

    text = 'tips:["tip1", "tip2"]'
    assert fix_quotes(text) == text, "Les structures tips doivent être préservées"


if __name__ == "__main__":
    pytest.main([__file__])

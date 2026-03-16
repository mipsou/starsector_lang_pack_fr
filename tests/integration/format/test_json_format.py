#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests d'intégration pour la validation du format JSON Starsector.
Ces tests vérifient que le format respecte exactement les conventions du jeu.
"""

import pytest
from pathlib import Path
import sys

# Ajout du chemin racine pour les imports
root_path = str(Path(__file__).parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

from integration.utils.format_helpers import validate_starsector_format, remove_comments

# Fixtures de test
@pytest.fixture
def valid_json():
    return '''{
\t"key":"value",
\t"array":[
\t\t"item1",
\t\t"item2",
\t],
\t"object":{
\t\t"nested":"value",
\t},
}'''

@pytest.fixture
def invalid_spacing():
    return '''{
\t"key": "value",
}'''

@pytest.fixture
def invalid_quotes():
    return '''{
\t"key":"«value»",
}'''

@pytest.fixture
def commented_json():
    return '''{
\t"key":"value", # Commentaire
\t# Autre commentaire
\t"array":[],
}'''

def test_original_format(valid_json):
    """Vérifie que le format original est correctement détecté comme valide."""
    errors = validate_starsector_format(valid_json)
    assert not errors, f"Le format original devrait être valide, erreurs: {errors}"

def test_spacing_rules(invalid_spacing):
    """Vérifie que les espaces après les deux points sont détectés."""
    errors = validate_starsector_format(invalid_spacing)
    assert errors
    assert any("Espace trouvé après les deux points" in error for error in errors)

def test_quote_rules(invalid_quotes):
    """Vérifie que les guillemets français sont détectés."""
    errors = validate_starsector_format(invalid_quotes)
    assert errors
    assert any("Guillemets français trouvés" in error for error in errors)

def test_comment_handling(commented_json):
    """Vérifie que les commentaires sont correctement gérés."""
    content_no_comments = remove_comments(commented_json)
    assert "#" not in content_no_comments
    errors = validate_starsector_format(content_no_comments)
    assert not errors

if __name__ == "__main__":
    pytest.main([__file__])

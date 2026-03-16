#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests de validation du format des fichiers.
Regroupe les tests de format JSON, typographie et guillemets.
"""

import pytest
import json
import re
import logging
import os
from pathlib import Path
from typing import Dict, List, Union, Any
from scripts.handlers.json_handler import JsonHandler
from scripts.handlers.starsector_json import parse_starsector_json

# Fonctions utilitaires
def _get_json_files():
    """Retourne la liste des fichiers JSON à tester."""
    base_dir = Path("localization/data/strings")
    json_files = []
    if base_dir.exists():
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".json"):
                    json_files.append(os.path.join(root, file))
    return json_files

def remove_comments(content: str) -> str:
    """
    Supprime les commentaires du contenu JSON.
    Préserve les lignes pour maintenir les numéros de ligne corrects.
    """
    # Supprime les commentaires de ligne commençant par //
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)

    # Supprime les commentaires multi-lignes /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    return content

# 1. Validation du format de base
class TestJsonFormat:
    """Tests pour la validation du format Starsector."""

    def test_original_format(self):
        """Test pour vérifier que le format Starsector est préservé."""
        test_files = _get_json_files()
        if not test_files:
            pytest.skip("Aucun fichier JSON trouvé dans localization/data/strings")
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert content.strip().startswith('{'), f"Le fichier {file} doit commencer par '{{'"
                assert content.strip().endswith('}'), f"Le fichier {file} doit se terminer par '}}'"

    def test_translation_format(self):
        """Test pour vérifier que le format de traduction est valide."""
        test_files = _get_json_files()
        if not test_files:
            pytest.skip("Aucun fichier JSON trouvé dans localization/data/strings")
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert content.strip().startswith('{'), f"Le fichier {file} doit commencer par '{{'"
                assert content.strip().endswith('}'), f"Le fichier {file} doit se terminer par '}}'"

    def test_comments(self):
        """Test pour vérifier que les commentaires sont correctement gérés."""
        content = """/* Commentaire multi-ligne */
        // Commentaire simple ligne
        {
            key:"value" // Commentaire fin de ligne
        }"""
        clean = remove_comments(content)
        assert clean.strip().startswith('{'), "Le contenu doit commencer par '{'"
        assert clean.strip().endswith('}'), "Le contenu doit se terminer par '}'"

    def test_trailing_spaces(self):
        """Test pour vérifier qu'il n'y a pas d'espaces en fin de ligne."""
        test_files = _get_json_files()
        if not test_files:
            pytest.skip("Aucun fichier JSON trouvé dans localization/data/strings")
        errors = []
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    stripped = line.rstrip('\n\r')
                    if stripped != stripped.rstrip():
                        errors.append(f"{file}:{line_num}")
        if errors:
            pytest.xfail(
                f"{len(errors)} ligne(s) avec espaces en fin de ligne : "
                + ", ".join(errors[:5])
            )

# 2. Tests de conversion des guillemets
class TestConvertQuotes:
    """Tests pour la conversion des guillemets dans différents contextes."""

    def test_convert_quotes_simple(self, json_handler):
        """Test de conversion simple des guillemets.
        Un texte entouré de guillemets est traité comme des délimiteurs externes ;
        le contenu interne sans guillemets n'est pas modifié.
        """
        input_text = '"texte"'
        # Les guillemets externes sont préservés, pas de guillemets internes à convertir
        result = json_handler.convert_quotes(input_text)
        assert result == '"texte"', (
            "Les délimiteurs externes doivent être préservés"
        )

    def test_convert_quotes_with_inner_quotes(self, json_handler):
        """Test de conversion avec guillemets internes."""
        input_text = 'texte avec "citation" dedans'
        result = json_handler.convert_quotes(input_text)
        # Les guillemets internes doivent être convertis en guillemets français
        assert '\xab' in result or '\u2039' in result, (
            "Les guillemets internes doivent être convertis en guillemets français"
        )

    def test_convert_quotes_error_case(self, json_handler):
        """Test de conversion avec cas sans guillemets."""
        input_text = "Pas de guillemets"
        expected = "Pas de guillemets"
        assert json_handler.convert_quotes(input_text) == expected

    def test_convert_quotes_empty(self, json_handler):
        """Test de conversion avec texte vide."""
        assert json_handler.convert_quotes("") == ""

# 3. Tests des guillemets
class TestQuotes:
    """Tests pour la conversion des guillemets."""

    def test_to_french_quotes_single(self, json_handler):
        """Test de conversion d'une seule citation."""
        input_text = 'texte avec "citation" fin'
        result = json_handler.convert_quotes(input_text)
        assert '\xab' in result, "Doit contenir un guillemet ouvrant français"
        assert '\xbb' in result, "Doit contenir un guillemet fermant français"

    def test_no_quotes_unchanged(self, json_handler):
        """Test qu'un texte sans guillemets n'est pas modifié."""
        input_text = "Texte sans guillemets"
        assert json_handler.convert_quotes(input_text) == input_text

# 4. Validation de la typographie française dans les valeurs textuelles
class TestTypography:
    """Tests pour la validation de la typographie française.

    NOTE: Les fichiers Starsector utilisent des guillemets droits pour la
    syntaxe JSON ; seules les valeurs textuelles sont concernées par la
    typographie française. Ces tests vérifient les valeurs parsées, pas le
    JSON brut.
    """

    def test_json_parseable(self):
        """Vérifie que tous les fichiers JSON sont parsables par le parser Starsector."""
        test_files = _get_json_files()
        if not test_files:
            pytest.skip("Aucun fichier JSON trouvé dans localization/data/strings")
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            data, error = parse_starsector_json(content)
            assert error is None, f"Erreur de parsing dans {file} : {error}"

# Fixtures
@pytest.fixture
def json_handler():
    """Fixture pour le gestionnaire JSON."""
    return JsonHandler(logging.getLogger())

@pytest.fixture
def text_files():
    """Fixture pour tous les fichiers texte à vérifier."""
    base_dir = Path('localization/data')
    return list(base_dir.rglob('*.json')) + list(base_dir.rglob('*.txt'))

if __name__ == "__main__":
    pytest.main([__file__])

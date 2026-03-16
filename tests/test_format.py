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

# Fonctions utilitaires
def _get_json_files():
    """Retourne la liste des fichiers JSON à tester."""
    base_dir = Path("localization/fr/data/strings")
    json_files = []
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
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Vérifier que le contenu est structuré correctement
                assert content.strip().startswith('{'), f"Le fichier {file} doit commencer par '{{'"
                assert content.strip().endswith('}'), f"Le fichier {file} doit se terminer par '}}'"

    def test_translation_format(self):
        """Test pour vérifier que le format de traduction est valide."""
        test_files = _get_json_files()
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Vérifier que le contenu est structuré correctement pour Starsector
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
        # Vérifier que le contenu nettoyé est valide pour Starsector
        assert clean.strip().startswith('{'), "Le contenu doit commencer par '{{'"
        assert clean.strip().endswith('}'), "Le contenu doit se terminer par '}}'"

    def test_trailing_spaces(self):
        """Test pour vérifier l'indentation avec des tabulations."""
        test_files = _get_json_files()
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    # Vérifier qu'il n'y a pas d'espaces en fin de ligne
                    if line.rstrip() != line.rstrip(' \n\r'):
                        assert False, f"Espace(s) en fin de ligne dans {file}:{line_num}"

# 2. Tests de conversion des guillemets
class TestConvertQuotes:
    """Tests pour la conversion des guillemets dans différents contextes."""
    
    def test_convert_quotes_simple(self, json_handler):
        """Test de conversion simple des guillemets."""
        input_text = "\"texte\""
        expected = "« texte »"
        assert json_handler.convert_quotes(input_text) == expected

    def test_convert_quotes_nested(self, json_handler):
        """Test de conversion des guillemets imbriqués."""
        input_text = "\"Texte \\\"citation\\\" fin\""
        expected = "« Texte « citation » fin »"
        assert json_handler.convert_quotes(input_text) == expected

    def test_convert_quotes_with_apostrophe(self, json_handler):
        """Test de conversion avec apostrophes."""
        input_text = "\"L'exemple\""
        expected = "« L'exemple »"
        assert json_handler.convert_quotes(input_text) == expected

    def test_convert_quotes_error_case(self, json_handler):
        """Test de conversion avec cas d'erreur."""
        input_text = "Pas de guillemets"
        expected = "Pas de guillemets"
        assert json_handler.convert_quotes(input_text) == expected

# 3. Tests des guillemets
class TestQuotes:
    """Tests pour la conversion des guillemets."""
    
    def test_to_french_quotes(self, json_handler):
        """Test de conversion en guillemets français."""
        input_text = "Ceci est un \"test\" avec des \"guillemets\""
        expected = "Ceci est un « test » avec des « guillemets »"
        output = json_handler.convert_quotes(input_text)
        assert output == expected, "La conversion en guillemets français a échoué"

    def test_nested_quotes(self, json_handler):
        """Test des guillemets imbriqués."""
        input_json = {
            "text": "Il a dit \"Je pense que c'est un \\\"excellent\\\" choix\" hier"
        }
        expected = {
            "text": "Il a dit « Je pense que c'est un « excellent » choix » hier"
        }
        output = json_handler.convert_quotes(json.dumps(input_json))
        output = json.loads(output)
        assert output == expected, "La gestion des guillemets imbriqués a échoué"

# 4. Validation de la typographie française
class TestTypography:
    """Tests pour la validation de la typographie française."""
    
    def test_quotes(self):
        """Test pour vérifier l'utilisation des guillemets."""
        test_files = _get_json_files()
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '"' not in content, f"Guillemets droits trouvés dans {file}"

    def test_spaces_before_punctuation(self):
        """Test pour vérifier les espaces avant la ponctuation."""
        test_files = _get_json_files()
        for file in test_files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    # Vérifier les espaces avant la ponctuation
                    if re.search(r'[^ ][:;!?]', line):
                        assert False, f"Espace manquant avant ponctuation dans {file}:{line_num}"

# Fixtures
@pytest.fixture
def json_handler():
    """Fixture pour le gestionnaire JSON."""
    return JsonHandler(logging.getLogger())

@pytest.fixture
def text_files():
    """Fixture pour tous les fichiers texte à vérifier."""
    base_dir = Path('localization/fr/data')
    return list(base_dir.rglob('*.json')) + list(base_dir.rglob('*.txt'))

if __name__ == "__main__":
    pytest.main([__file__])

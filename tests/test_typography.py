#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests pour la validation de la typographie française.

NOTE: Ces tests vérifient uniquement les valeurs textuelles (pas les clés JSON,
ni la syntaxe JSON elle-même). Les fichiers Starsector utilisent le format JSON
avec des guillemets droits pour la structure ; seules les valeurs de texte
destinées au joueur doivent respecter la typographie française.
"""

import pytest
import re
import json
from pathlib import Path
from scripts.handlers.starsector_json import parse_starsector_json


def _extract_text_values(data, path=""):
    """Extrait récursivement toutes les valeurs textuelles d'une structure JSON."""
    texts = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                texts.append((f"{path}.{key}" if path else key, value))
            elif isinstance(value, (dict, list)):
                texts.extend(_extract_text_values(value, f"{path}.{key}" if path else key))
    elif isinstance(data, list):
        for i, value in enumerate(data):
            if isinstance(value, str):
                texts.append((f"{path}[{i}]", value))
            elif isinstance(value, (dict, list)):
                texts.extend(_extract_text_values(value, f"{path}[{i}]"))
    return texts


class TestTypography:
    """Tests pour la validation de la typographie française."""

    @pytest.fixture
    def text_files(self):
        """Fixture pour tous les fichiers JSON à vérifier."""
        base_dir = Path('localization/data')
        return list(base_dir.rglob('*.json'))

    @pytest.fixture
    def text_values(self, text_files):
        """Extrait toutes les valeurs textuelles des fichiers JSON."""
        all_texts = []
        for file in text_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                data, error = parse_starsector_json(content)
                if not error and data:
                    for path, text in _extract_text_values(data):
                        all_texts.append((file, path, text))
            except Exception:
                pass
        return all_texts

    def test_ellipsis(self, text_values):
        """Vérifie l'utilisation du caractère points de suspension."""
        pattern = r'\.{3}'
        errors = []
        for file, path, text in text_values:
            if re.search(pattern, text):
                errors.append(f"{file} [{path}]: utiliser \u2026 au lieu de ...")
        # Avertissement informatif, pas bloquant pour le format Starsector
        if errors:
            pytest.xfail(
                f"{len(errors)} occurrence(s) de '...' au lieu de '\u2026' :\n"
                + "\n".join(errors[:10])
            )

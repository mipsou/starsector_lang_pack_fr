#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import re
from pathlib import Path

class TestTypography:
    """Tests pour la validation de la typographie française."""
    
    @pytest.fixture
    def text_files(self):
        """Fixture pour tous les fichiers texte à vérifier."""
        base_dir = Path('localization/fr/data')
        return list(base_dir.rglob('*.json')) + list(base_dir.rglob('*.txt'))
    
    def test_spaces_before_punctuation(self, text_files):
        """Vérifie les espaces avant les signes de ponctuation doubles."""
        pattern = r'[^\s][;:!?»]'
        for file in text_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.finditer(pattern, content)
                errors = []
                for match in matches:
                    pos = match.start()
                    line_num = content.count('\n', 0, pos) + 1
                    errors.append(f"Ligne {line_num}: espace manquant avant '{match.group()}'")
                assert not errors, f"\nErreurs dans {file}:\n" + "\n".join(errors)
    
    def test_spaces_after_punctuation(self, text_files):
        """Vérifie les espaces après les signes de ponctuation."""
        pattern = r'[;:!?«][^\s]'
        for file in text_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.finditer(pattern, content)
                errors = []
                for match in matches:
                    pos = match.start()
                    line_num = content.count('\n', 0, pos) + 1
                    errors.append(f"Ligne {line_num}: espace manquant après '{match.group()}'")
                assert not errors, f"\nErreurs dans {file}:\n" + "\n".join(errors)
    
    def test_quotation_marks(self, text_files):
        """Vérifie l'utilisation des guillemets français."""
        pattern = r'"[^"]*"'
        for file in text_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.finditer(pattern, content)
                errors = []
                for match in matches:
                    pos = match.start()
                    line_num = content.count('\n', 0, pos) + 1
                    errors.append(f"Ligne {line_num}: utiliser « » au lieu de \"{match.group()}\"")
                assert not errors, f"\nErreurs dans {file}:\n" + "\n".join(errors)
    
    def test_ellipsis(self, text_files):
        """Vérifie l'utilisation du caractère points de suspension."""
        pattern = r'\.{3}'
        for file in text_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.finditer(pattern, content)
                errors = []
                for match in matches:
                    pos = match.start()
                    line_num = content.count('\n', 0, pos) + 1
                    errors.append(f"Ligne {line_num}: utiliser … au lieu de ...")
                assert not errors, f"\nErreurs dans {file}:\n" + "\n".join(errors)

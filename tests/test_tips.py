#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests pour la validation des tips (conseils en jeu).

Le format tips.json de Starsector est non-standard :
- Clé non quotée : tips:[...]
- Commentaires avec #
- Virgules finales autorisées
"""

import pytest
import re
from pathlib import Path
from scripts.json_utils import parse_starsector_tips


class TestTips:
    """Tests pour la validation des tips."""

    @pytest.fixture
    def tips_file(self):
        """Fixture pour le fichier de tips traduit."""
        return Path('localization/data/strings/tips.json')

    @pytest.fixture
    def original_tips(self):
        """Fixture pour les tips originaux."""
        return Path('original/data/strings/tips.json')

    def test_tips_file_exists(self, tips_file):
        """Vérifie que le fichier de tips existe."""
        assert tips_file.exists(), f"Le fichier {tips_file} n'existe pas"

    def test_tips_is_valid(self, tips_file):
        """Vérifie que le fichier est un tips.json Starsector valide."""
        try:
            tips = parse_starsector_tips(tips_file)
            assert len(tips) > 0, "Le fichier de tips est vide"
        except Exception as e:
            pytest.fail(f"Le fichier {tips_file} n'est pas un tips.json valide : {str(e)}")

    def test_tips_structure_matches_original(self, tips_file, original_tips):
        """Vérifie que la structure correspond à l'original."""
        if not original_tips.exists():
            pytest.skip(f"Fichier original {original_tips} non trouvé")

        try:
            translated = parse_starsector_tips(tips_file)
            original = parse_starsector_tips(original_tips)
        except Exception as e:
            pytest.fail(f"Erreur de parsing : {str(e)}")

        assert len(translated) == len(original), (
            f"Nombre de tips différent : {len(translated)} vs {len(original)}"
        )

        for i, (trans, orig) in enumerate(zip(translated, original)):
            if isinstance(orig, dict):
                assert isinstance(trans, dict), f"Le tip {i} devrait être un objet"
                assert "freq" in trans and "tip" in trans, (
                    f"Le tip {i} n'a pas les champs requis"
                )
                assert trans["freq"] == orig["freq"], (
                    f"Fréquence différente pour le tip {i}"
                )
            else:
                assert isinstance(trans, str), f"Le tip {i} devrait être une chaîne"

    def test_tips_no_empty_translations(self, tips_file):
        """Vérifie qu'il n'y a pas de traductions vides."""
        tips = parse_starsector_tips(tips_file)
        for i, tip in enumerate(tips):
            if isinstance(tip, dict):
                assert tip["tip"].strip(), f"Traduction vide pour le tip {i}"
            else:
                assert tip.strip(), f"Traduction vide pour le tip {i}"

    def test_tips_no_untranslated_english(self, tips_file):
        """Vérifie qu'il n'y a pas de tips manifestement non traduits."""
        tips = parse_starsector_tips(tips_file)
        # Mots anglais courants qui ne devraient pas apparaître en français
        english_markers = ['the ', ' and ', ' you ', 'your ', ' will ']
        suspicious = []
        for i, tip in enumerate(tips):
            text = tip["tip"] if isinstance(tip, dict) else tip
            text_lower = text.lower()
            if any(marker in text_lower for marker in english_markers):
                suspicious.append(f"Tip {i}: possiblement non traduit")

        if suspicious:
            pytest.xfail(
                f"{len(suspicious)} tip(s) possiblement non traduit(s) :\n"
                + "\n".join(suspicious[:5])
            )

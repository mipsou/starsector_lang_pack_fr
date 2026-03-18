#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests pour la validation des missions.

Les missions Starsector sont des fichiers mission_text.txt dans des sous-répertoires
de localization/data/missions/ (un répertoire par mission).
"""

import pytest
from pathlib import Path


class TestMissions:
    """Tests pour la validation des missions."""

    @pytest.fixture
    def missions_dir(self):
        """Fixture pour le répertoire des missions traduites."""
        return Path('localization/data/missions')

    @pytest.fixture
    def original_missions_dir(self):
        """Fixture pour le répertoire original des missions."""
        return Path('original/data/missions')

    def test_missions_dir_exists(self, missions_dir):
        """Vérifie que le répertoire des missions existe."""
        assert missions_dir.exists(), f"Le répertoire {missions_dir} n'existe pas"
        assert missions_dir.is_dir(), f"{missions_dir} n'est pas un répertoire"

    def test_translated_missions_valid(self, missions_dir, original_missions_dir):
        """Vérifie que les missions traduites correspondent à des missions originales."""
        if not original_missions_dir.exists():
            pytest.skip(f"Répertoire original {original_missions_dir} non trouvé")

        # Les missions sont des sous-répertoires contenant mission_text.txt
        original_missions = {
            d.name for d in original_missions_dir.iterdir()
            if d.is_dir() and (d / 'mission_text.txt').exists()
        }
        translated_missions = {
            d.name for d in missions_dir.iterdir()
            if d.is_dir() and (d / 'mission_text.txt').exists()
        }

        # Vérifie qu'il n'y a pas de missions traduites sans original
        extra_missions = translated_missions - original_missions
        assert not extra_missions, f"Missions traduites sans original : {extra_missions}"

        # Informe sur la couverture (non bloquant)
        missing_missions = original_missions - translated_missions
        if missing_missions:
            coverage = len(translated_missions) / len(original_missions) * 100
            print(f"\nCouverture missions : {coverage:.0f}% ({len(translated_missions)}/{len(original_missions)})")
            print(f"Missions non traduites : {missing_missions}")

    def test_missions_text_not_empty(self, missions_dir):
        """Vérifie que les fichiers mission_text.txt ne sont pas vides."""
        empty_files = []
        for mission_dir in missions_dir.iterdir():
            if mission_dir.is_dir():
                text_file = mission_dir / 'mission_text.txt'
                if text_file.exists():
                    content = text_file.read_text(encoding='utf-8').strip()
                    if not content:
                        empty_files.append(str(text_file))

        assert not empty_files, f"Fichiers mission_text.txt vides : {empty_files}"

    def test_missions_encoding(self, missions_dir):
        """Vérifie que les fichiers de mission sont en UTF-8."""
        import chardet
        encoding_errors = []
        for mission_dir in missions_dir.iterdir():
            if mission_dir.is_dir():
                text_file = mission_dir / 'mission_text.txt'
                if text_file.exists():
                    raw = text_file.read_bytes()
                    result = chardet.detect(raw)
                    detected = result.get('encoding', '')
                    if detected and detected.lower().replace('-', '') not in ('utf8', 'ascii'):
                        encoding_errors.append(
                            f"{text_file}: {detected}"
                        )

        assert not encoding_errors, (
            f"Fichiers non UTF-8 :\n" + "\n".join(encoding_errors)
        )

    def test_mission_list_csv(self, missions_dir):
        """Vérifie que mission_list.csv existe et est valide."""
        import csv
        csv_file = missions_dir / 'mission_list.csv'
        if not csv_file.exists():
            pytest.skip("mission_list.csv non trouvé")

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert len(headers) > 0, "mission_list.csv n'a pas d'en-têtes"

            row_errors = []
            for i, row in enumerate(reader, 2):
                if len(row) != len(headers):
                    row_errors.append(
                        f"Ligne {i}: {len(row)} colonnes au lieu de {len(headers)}"
                    )

        assert not row_errors, f"Erreurs CSV :\n" + "\n".join(row_errors)

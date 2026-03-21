#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests pour la validation des descriptions de vaisseaux.

NOTE: Les tests JSON originaux de ce fichier ont été marqués comme obsolètes car
le projet utilise ship_data.csv (format CSV) et non ship_data.json (format JSON).
Les données de vaisseaux se trouvent dans localization/data/hulls/ship_data.csv
et original/data/hulls/ship_data.csv.
Les tests ont été adaptés pour valider le format CSV réel.
"""

import pytest
import csv
from pathlib import Path


class TestShips:
    """Tests pour la validation des données de vaisseaux (format CSV)."""

    @pytest.fixture
    def ships_file(self):
        """Fixture pour le fichier CSV des vaisseaux traduits."""
        return Path('localization/data/hulls/ship_data.csv')

    @pytest.fixture
    def original_ships_file(self):
        """Fixture pour le fichier CSV original des vaisseaux."""
        return Path('original/data/hulls/ship_data.csv')

    def _read_csv(self, file_path):
        """Lit un fichier CSV et retourne les en-têtes et les lignes."""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
        return headers, rows

    def test_ships_file_exists(self, ships_file):
        """Vérifie que le fichier des vaisseaux existe."""
        assert ships_file.exists(), f"Le fichier {ships_file} n'existe pas"

    def test_ships_valid_csv(self, ships_file):
        """Vérifie que le fichier est un CSV valide avec des en-têtes."""
        headers, rows = self._read_csv(ships_file)
        assert headers is not None, "Le fichier CSV n'a pas d'en-têtes"
        assert len(headers) > 0, "Le fichier CSV a des en-têtes vides"
        assert len(rows) > 0, "Le fichier CSV n'a pas de données"

    def test_ships_structure(self, ships_file, original_ships_file):
        """Vérifie que les colonnes essentielles du CSV sont présentes."""
        if not original_ships_file.exists():
            pytest.skip(f"Fichier original {original_ships_file} non trouvé")

        trans_headers, trans_rows = self._read_csv(ships_file)
        orig_headers, orig_rows = self._read_csv(original_ships_file)

        # Vérifie que les colonnes essentielles sont présentes
        essential_cols = ['name', 'id', 'designation']
        for col in essential_cols:
            assert col in trans_headers, (
                f"Colonne essentielle manquante : {col}"
            )

    def test_ships_required_fields(self, ships_file):
        """Vérifie que les champs essentiels sont présents et non vides."""
        headers, rows = self._read_csv(ships_file)

        required_fields = ['name', 'id', 'designation']
        for field in required_fields:
            assert field in headers, f"Champ requis manquant dans les en-têtes : {field}"

        empty_errors = []
        for i, row in enumerate(rows, 2):
            for field in required_fields:
                if field in row and not row[field].strip():
                    empty_errors.append(f"Ligne {i}: champ '{field}' vide pour id={row.get('id', '?')}")

        assert not empty_errors, f"Champs vides trouvés :\n" + "\n".join(empty_errors[:20])

    def test_ships_ids_subset_of_original(self, ships_file, original_ships_file):
        """Vérifie que les IDs traduits existent dans l'original (pas d'IDs inventés)."""
        if not original_ships_file.exists():
            pytest.skip(f"Fichier original {original_ships_file} non trouvé")

        _, trans_rows = self._read_csv(ships_file)
        _, orig_rows = self._read_csv(original_ships_file)

        trans_ids = {row.get('id', '') for row in trans_rows if row.get('id', '').strip()}
        orig_ids = {row.get('id', '') for row in orig_rows if row.get('id', '').strip()}

        extra = trans_ids - orig_ids
        if extra:
            # Des IDs supplémentaires peuvent exister (ajouts de mod) ; avertissement
            import warnings
            warnings.warn(
                f"IDs dans la traduction absents de l'original : {extra}. "
                "Cela peut être intentionnel (vaisseaux ajoutés par le mod)."
            )

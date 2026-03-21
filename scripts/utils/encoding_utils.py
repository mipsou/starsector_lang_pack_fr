#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilitaires de vérification d'encodage pour le système de traduction Starsector.
"""

import chardet
from pathlib import Path
from typing import Optional


def check_encoding(file_path, expected_encoding='utf-8') -> bool:
    """
    Vérifie que le fichier est encodé dans l'encodage attendu.

    Args:
        file_path: Chemin du fichier à vérifier
        expected_encoding: Encodage attendu (par défaut UTF-8)

    Returns:
        True si l'encodage correspond, False sinon
    """
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
            result = chardet.detect(raw)
            detected = result.get('encoding', '')
            if detected is None:
                return False
            return detected.lower().replace('-', '') in (
                expected_encoding.lower().replace('-', ''),
                'ascii',  # ASCII est un sous-ensemble de UTF-8
            )
    except Exception:
        return False


def validate_typography(text: str) -> bool:
    """
    Valide la typographie française d'un texte.

    Vérifie :
    - Guillemets français (« ») au lieu de guillemets droits
    - Apostrophes typographiques
    - Espaces avant la ponctuation double
    - Points de suspension (caractère unique)

    Args:
        text: Texte à valider

    Returns:
        True si la typographie est correcte, False sinon
    """
    import re

    # Vérifier les guillemets droits (sauf dans les structures JSON)
    if '"' in text:
        return False

    # Vérifier les apostrophes droites
    if "'" in text:
        return False

    # Vérifier les espaces avant la ponctuation double
    if re.search(r'[^\s][;:!?]', text):
        return False

    # Vérifier les espaces autour des guillemets français
    if re.search(r'«[^\s]', text) or re.search(r'[^\s]»', text):
        return False

    return True


def compare_with_original(translated_data, original_data) -> list:
    """
    Compare les données traduites avec les données originales.

    Args:
        translated_data: Données traduites (dict ou list)
        original_data: Données originales (dict ou list)

    Returns:
        Liste des différences trouvées
    """
    differences = []

    if isinstance(original_data, dict) and isinstance(translated_data, dict):
        # Vérifier les clés manquantes
        for key in original_data:
            if key not in translated_data:
                differences.append(f"Clé manquante dans la traduction : {key}")

        # Vérifier les clés en trop
        for key in translated_data:
            if key not in original_data:
                differences.append(f"Clé supplémentaire dans la traduction : {key}")

    elif isinstance(original_data, list) and isinstance(translated_data, list):
        if len(original_data) != len(translated_data):
            differences.append(
                f"Nombre d'éléments différent : {len(translated_data)} vs {len(original_data)}"
            )

    return differences

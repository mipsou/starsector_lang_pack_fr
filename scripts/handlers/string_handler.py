#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion des chaînes de caractères pour la traduction française de Starsector.

Ce module gère :
1. La conversion des guillemets selon les règles typographiques françaises
2. Le respect des formats JSON spécifiques de Starsector
3. La gestion des espaces autour de la ponctuation

Formats JSON supportés :
- Tips : tableau simple de strings
- Tooltips : structure hiérarchique à 2-3 niveaux
- Strings : structure à 2 niveaux avec variables
"""

import regex
import logging
from typing import Union, Dict, List, Any

# Configuration du logging
logger = logging.getLogger(__name__)

# Constantes typographiques
ESPACE_FINE = '\u202F'  # Espace fine insécable
PUNCTUATION_INSIDE = [',', '.']  # Ponctuation toujours à l'intérieur des guillemets
PUNCTUATION_OUTSIDE = ['?', '!', ';']  # Ponctuation à l'extérieur avec espace

class StringHandler:
    """Gestionnaire des chaînes de caractères avec support des règles typographiques françaises."""
    
    def __init__(self):
        """Initialise le gestionnaire de chaînes."""
        self.logger = logging.getLogger(__name__)
    
    def process_quotes(self, text: str, level: int = 0) -> str:
        """
        Traite récursivement les citations dans le texte.

        Pour le niveau 0 (premier niveau de citation dans le contenu interne),
        on utilise des guillemets doubles typographiques (« … »).
        Pour les niveaux supérieurs (citations imbriquées), on utilise des guillemets simples (‹ … ›).

        La ponctuation est gérée selon les règles typographiques françaises :
        - La virgule et le point sont toujours à l'intérieur des guillemets
        - Le point d'interrogation, d'exclamation et le point-virgule peuvent être à l'extérieur
          avec un espace entre le guillemet fermant et la ponctuation

        Args:
            text (str): Le texte à traiter
            level (int): Le niveau d'imbrication actuel (0 = premier niveau)

        Returns:
            str: Le texte avec les guillemets convertis
        """
        # Pattern récursif qui repère une séquence encadrée par des guillemets non échappés
        pattern = r'"((?:[^"\\]+|\\.|(?R))*)"'
        
        def replacer(match):
            inner = match.group(1)
            # On traite récursivement le contenu pour détecter d'éventuelles citations imbriquées
            processed_inner = self.process_quotes(inner, level + 1)
            
            # Gestion de la ponctuation finale
            trailing = ""
            stripped = processed_inner.rstrip()
            if stripped:
                last_char = stripped[-1]
                # Si c'est une ponctuation qui doit être à l'intérieur, on la garde
                if last_char in PUNCTUATION_INSIDE:
                    processed_inner = stripped
                # Si c'est une ponctuation qui peut être à l'extérieur, on la déplace
                elif last_char in PUNCTUATION_OUTSIDE:
                    trailing = " " + last_char  # Ajout d'un espace avant la ponctuation
                    processed_inner = stripped[:-1].rstrip()
            
            # Choix des guillemets en fonction du niveau d'imbrication
            if level == 0:
                # Premier niveau de citation interne → guillemets doubles typographiques
                opening = '«\u202F'
                closing = '\u202F»'
            else:
                # Deuxième niveau (et au-delà) → guillemets simples typographiques
                opening = '‹\u202F'
                closing = '\u202F›'
            
            return opening + processed_inner + closing + trailing

        return regex.sub(pattern, replacer, text)

    def convert_json_string(self, text: str) -> str:
        """
        Convertit une chaîne de caractères JSON en respectant les règles typographiques françaises.
        Préserve les guillemets externes du JSON.

        Args:
            text (str): La chaîne à convertir

        Returns:
            str: La chaîne convertie
        """
        # Si la chaîne est vide ou None, on la retourne telle quelle
        if not text:
            return text

        # On ne traite que l'intérieur des guillemets JSON
        if text.startswith('"') and text.endswith('"'):
            inner = text[1:-1]
            converted = self.process_quotes(inner)
            return f'"{converted}"'
        
        return text

    def convert_json_value(self, value: Any) -> Any:
        """
        Convertit récursivement une valeur JSON en appliquant les règles typographiques françaises.

        Args:
            value: La valeur à convertir (peut être un dict, une liste, une chaîne ou autre)

        Returns:
            La valeur convertie
        """
        if isinstance(value, dict):
            return {k: self.convert_json_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.convert_json_value(item) for item in value]
        elif isinstance(value, str):
            return self.convert_json_string(value)
        return value

    def convert_json_content(self, content: Union[Dict, List]) -> Union[Dict, List]:
        """
        Convertit le contenu d'un fichier JSON en appliquant les règles typographiques françaises.

        Args:
            content: Le contenu JSON à convertir (dict ou liste)

        Returns:
            Le contenu converti
        """
        return self.convert_json_value(content)

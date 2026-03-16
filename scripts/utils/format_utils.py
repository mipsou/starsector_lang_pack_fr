#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilitaires de formatage pour les fichiers Starsector.
Gère la normalisation des guillemets, espaces et autres éléments de formatage.
"""

import re
from typing import Dict, List, Optional

class FormatUtils:
    """Utilitaires de formatage pour les fichiers Starsector."""
    
    @staticmethod
    def fix_quotes(text: str) -> str:
        """Normalise les guillemets dans un texte."""
        # Remplace les guillemets français par des guillemets droits
        text = text.replace('«', '"').replace('»', '"')
        text = text.replace('"', '"').replace('"', '"')
        
        # Normalise les apostrophes
        text = text.replace(''', "'").replace(''', "'")
        
        return text
    
    @staticmethod
    def normalize_newlines(text: str) -> str:
        """Normalise les sauts de ligne en style Unix."""
        return text.replace('\r\n', '\n').replace('\r', '\n')
    
    @staticmethod
    def remove_trailing_spaces(text: str) -> str:
        """Supprime les espaces en fin de ligne."""
        return '\n'.join(line.rstrip() for line in text.splitlines())
    
    @staticmethod
    def fix_json_format(text: str) -> str:
        """Corrige le format JSON pour correspondre aux spécifications Starsector."""
        # Supprime les espaces après les deux points dans les clés
        text = re.sub(r'": ', '":"', text)
        text = re.sub(r'": \[', '":[', text)
        text = re.sub(r'": {', '":{', text)
        
        # Normalise l'indentation avec des tabulations
        lines = text.splitlines()
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            # Ajuste le niveau d'indentation
            if re.search(r'[}\]]', line.strip()):
                indent_level -= 1
            
            # Applique l'indentation
            if line.strip():
                formatted_lines.append('\t' * indent_level + line.strip())
            else:
                formatted_lines.append('')
            
            # Prépare le niveau d'indentation pour la prochaine ligne
            if re.search(r'[{\[]', line.strip()):
                indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def validate_format(text: str, format_rules: Dict[str, List[str]]) -> bool:
        """Valide le format d'un texte selon des règles spécifiques."""
        try:
            # Vérifie les motifs interdits
            if 'forbidden_patterns' in format_rules:
                for pattern in format_rules['forbidden_patterns']:
                    if re.search(pattern, text):
                        return False
            
            # Vérifie les motifs requis
            if 'required_patterns' in format_rules:
                for pattern in format_rules['required_patterns']:
                    if not re.search(pattern, text):
                        return False
            
            return True
            
        except Exception as e:
            return False

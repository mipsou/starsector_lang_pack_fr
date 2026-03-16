#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions utilitaires pour la validation du format JSON Starsector.
Ces fonctions sont utilisées par les tests d'intégration.
"""

from typing import List, Dict, Union, Any
import re

def remove_comments(content: str) -> str:
    """
    Supprime les commentaires du contenu JSON.
    Préserve les lignes pour maintenir les numéros de ligne corrects.
    
    Args:
        content: Contenu JSON avec commentaires
        
    Returns:
        str: Contenu sans commentaires
    
    Example:
        >>> content = '{"key": "value"} # commentaire\\n'
        >>> remove_comments(content)
        '{"key": "value"}             \\n'
    """
    lines = []
    for line in content.split('\n'):
        if '#' in line:
            comment_start = line.index('#')
            line = line[:comment_start] + ' ' * (len(line) - comment_start)
        lines.append(line)
    return '\n'.join(lines)

def validate_starsector_format(content: str) -> List[str]:
    """
    Valide le format exact d'un contenu JSON selon les règles Starsector.
    
    Args:
        content: Contenu JSON à valider
        
    Returns:
        List[str]: Liste des erreurs trouvées. Liste vide si aucune erreur.
    
    Règles validées:
    1. Pas d'espace après les deux points
    2. Indentation par tabulations
    3. Virgules finales obligatoires
    4. Guillemets droits uniquement
    """
    errors = []
    content_no_comments = remove_comments(content)
    
    # 1. Vérification des espaces après les deux points
    colon_spaces = re.finditer(r'":[\s]+[^\s]', content_no_comments)
    for match in colon_spaces:
        line_num = content_no_comments[:match.start()].count('\n') + 1
        errors.append(f"Ligne {line_num}: Espace trouvé après les deux points")
    
    # 2. Vérification de l'indentation
    lines = content_no_comments.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped and not stripped.startswith('#'):
            indent = len(line) - len(stripped)
            if indent > 0 and not line.startswith('\t' * (indent // 4)):
                errors.append(f"Ligne {i}: Indentation incorrecte (doit utiliser des tabulations)")
    
    # 3. Vérification des virgules finales
    stack = []
    in_string = False
    escape = False
    last_non_whitespace = None
    line_num = 1
    
    for i, char in enumerate(content_no_comments):
        if char == '\n':
            line_num += 1
            continue
            
        if char == '"' and not escape:
            in_string = not in_string
        elif char == '\\' and not escape:
            escape = True
            continue
            
        if not in_string:
            if char in '{[':
                stack.append((char, line_num))
            elif char in '}]':
                if stack:
                    opening, _ = stack.pop()
                    if (opening == '{' and char == '}') or (opening == '[' and char == ']'):
                        if last_non_whitespace not in {',', '{', '[', None}:
                            errors.append(f"Ligne {line_num}: Virgule finale manquante avant {char}")
            
        if not char.isspace():
            last_non_whitespace = char
        escape = False
    
    # 4. Vérification des guillemets
    quotes = re.finditer(r'[«»]', content_no_comments)
    for match in quotes:
        line_num = content_no_comments[:match.start()].count('\n') + 1
        errors.append(f"Ligne {line_num}: Guillemets français trouvés (utiliser des guillemets droits)")
    
    return errors

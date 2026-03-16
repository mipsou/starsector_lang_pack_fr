#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests de validation du format JSON Starsector.
Vérifie que le format respecte exactement les conventions du jeu.
"""

import pytest
import json
import re
from pathlib import Path
from typing import Dict, List, Union, Any

def remove_comments(content: str) -> str:
    """
    Supprime les commentaires du contenu JSON.
    Préserve les lignes pour maintenir les numéros de ligne corrects.
    
    Args:
        content: Contenu JSON avec commentaires
        
    Returns:
        Contenu sans commentaires
    """
    lines = []
    for line in content.split('\n'):
        # Remplace les commentaires par des espaces vides
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
        Liste des erreurs trouvées. Liste vide si aucune erreur.
    """
    errors = []
    
    # Supprime les commentaires pour l'analyse
    content_no_comments = remove_comments(content)
    
    # 1. Vérification des espaces après les deux points
    colon_spaces = re.finditer(r'":[\s]+[^\s]', content_no_comments)
    for match in colon_spaces:
        line_num = content_no_comments[:match.start()].count('\n') + 1
        errors.append(f"Ligne {line_num}: Espace trouvé après les deux points")
    
    # 2. Vérification de l'indentation (tabulations)
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

def test_original_format():
    """Vérifie que le format original est correctement détecté comme valide."""
    original_path = Path("d:/Fractal Softworks/Starsector/starsector-core/data/strings/tooltips.json")
    with open(original_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = validate_starsector_format(content)
    assert not errors, f"Le fichier original contient des erreurs : {errors}"

def test_translation_format():
    """Vérifie que notre traduction respecte le format."""
    translation_path = Path("d:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/tests/data/tooltips_fr.json")
    with open(translation_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = validate_starsector_format(content)
    assert not errors, f"La traduction contient des erreurs de format : {errors}"

def test_specific_format_rules():
    """Tests spécifiques pour chaque règle de formatage."""
    
    # Test 1: Pas d'espace après les deux points
    invalid_format = '{"key": "value"}'
    errors = validate_starsector_format(invalid_format)
    assert any("Espace trouvé après les deux points" in err for err in errors)
    
    # Test 2: Indentation avec tabulations
    invalid_format = '{\n    "key":"value"\n}'
    errors = validate_starsector_format(invalid_format)
    assert any("Indentation incorrecte" in err for err in errors)
    
    # Test 3: Virgules finales obligatoires
    invalid_format = '{\n\t"key1":"value1"\n\t"key2":"value2"\n}'
    errors = validate_starsector_format(invalid_format)
    assert any("Virgule finale manquante" in err for err in errors)
    
    # Test 4: Pas de guillemets français
    invalid_format = '{\n\t"key":"« value »"\n}'
    errors = validate_starsector_format(invalid_format)
    assert any("Guillemets français trouvés" in err for err in errors)

def test_comments():
    """Vérifie que les commentaires sont correctement gérés."""
    content = """
{
    #"commented_key": "value",
    "active_key":"value", # Commentaire en fin de ligne
    "last_key":"value"
}
"""
    errors = validate_starsector_format(content)
    # Ne devrait pas signaler d'erreur pour les lignes commentées
    assert not any("commented_key" in err for err in errors)

if __name__ == "__main__":
    pytest.main([__file__])

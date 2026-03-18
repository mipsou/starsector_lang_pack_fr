#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de correction des fichiers de traduction Starsector.
Se base sur les fonctions validées du projet.

Auteur: Mipsou
Date: 2025-01-31
"""

import json
import os
from pathlib import Path
import shutil
from datetime import datetime

# Table de correspondance pour les corrections de caractères
CHAR_MAP = {
    '\u00e9\u00e9\u00e9': '\u00e9',  # ééé -> é
    '\u00e9\u00e9': '\u00e9',        # éé -> é
    '\u00e9\u00e9\u00e0': '\u00e0',  # ééà -> à
    '\u00e9\u00e9\u00e2': '\u00e2',  # ééâ -> â
    '\u00e9\u00e9\u00e8': '\u00e8',  # ééè -> è
    '\u00e9\u00e9\u00ea': '\u00ea',  # ééê -> ê
    '\u00e9\u00e9\u00eb': '\u00eb',  # ééë -> ë
    '\u00e9\u00e9\u00ee': '\u00ee',  # ééî -> î
    '\u00e9\u00e9\u00ef': '\u00ef',  # ééï -> ï
    '\u00e9\u00e9\u00f4': '\u00f4',  # ééô -> ô
    '\u00e9\u00e9\u00f9': '\u00f9',  # ééù -> ù
    '\u00e9\u00e9\u00fb': '\u00fb',  # ééû -> û
    '\u00e9\u00e9\u00fc': '\u00fc',  # ééü -> ü
    '\u00e9\u00e9\u00ff': '\u00ff',  # ééÿ -> ÿ
    '\u00e9\u00e9\u00e7': '\u00e7',  # ééç -> ç
    '\u00e9\u00c2\u00e9': '\u00e9',  # éÂé -> é
    '\u00e2\u00c2': '\u00e2',        # âÂ -> â
    '\u00e9\u00c2': '\u00e9',        # éÂ -> é
    '\u00e9\u00e9\u00c2': '\u00e9'   # ééÂ -> é
}

def fix_special_chars(text):
    """
    Corrige les caractères spéciaux dans le texte.
    """
    # Table de conversion des caractères spéciaux
    char_map = {
        'é': 'é',
        'è': 'è',
        'à': 'à',
        'ù': 'ù',
        'â': 'â',
        'ê': 'ê',
        'î': 'î',
        'ô': 'ô',
        'û': 'û',
        'ë': 'ë',
        'ï': 'ï',
        'ü': 'ü',
        'ÿ': 'ÿ',
        'ç': 'ç',
        'œ': 'œ',
        'æ': 'æ',
        "'": "'",
        '"': '"',
        '"': '"',
        '«': '"',
        '»': '"',
        '…': '...',
        '–': '-',
        '—': '-'
    }
    
    for old, new in char_map.items():
        text = text.replace(old, new)
    
    return text

def remove_comments(content):
    """Supprime les commentaires du contenu JSON."""
    # Supprime les commentaires de ligne commençant par #
    lines = []
    for line in content.split('\n'):
        if '#' in line:
            comment_pos = line.find('#')
            # Vérifie si le # n'est pas dans une chaîne de caractères
            in_string = False
            for i in range(comment_pos):
                if line[i] == '"' and (i == 0 or line[i-1] != '\\'):
                    in_string = not in_string
            if not in_string:
                line = line[:comment_pos].rstrip()
        if line.strip():  # Garde seulement les lignes non vides
            lines.append(line)
    return '\n'.join(lines)

def validate_json_structure(content):
    """
    Valide la structure JSON et les caractères spéciaux.
    Retourne (True, None) si valide, (False, error_message) sinon.
    """
    try:
        # Supprime d'abord les commentaires
        clean_content = remove_comments(content)
        
        # Vérifie la structure JSON
        data = json.loads(clean_content)
        
        # Vérifie l'encodage des caractères spéciaux
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if not isinstance(subvalue, str):
                        return False, f"La valeur de {key}.{subkey} n'est pas une chaîne de caractères"
            elif not isinstance(value, str):
                return False, f"La valeur de {key} n'est pas une chaîne de caractères"
        
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Erreur inattendue : {str(e)}"

def fix_json_structure(translation_path, original_path):
    """
    Corrige la structure JSON du fichier de traduction en se basant sur l'original.
    Crée une sauvegarde avant modification.
    """
    # Crée une sauvegarde
    backup_path = f"{translation_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(translation_path, backup_path)
    print(f"Sauvegarde créée : {backup_path}")

    # Lit le fichier original
    with open(original_path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Lit le fichier de traduction
    with open(translation_path, 'r', encoding='utf-8') as f:
        translation = f.read()

    # Supprime les commentaires
    translation = remove_comments(translation)

    # Corrige les caractères spéciaux
    translation = fix_special_chars(translation)

    # Valide la structure
    is_valid, error = validate_json_structure(translation)
    if not is_valid:
        print(f"Erreur de structure JSON : {error}")
        return False

    # Écrit le fichier corrigé
    with open(translation_path, 'w', encoding='utf-8') as f:
        f.write(translation)

    print(f"Fichier corrigé : {translation_path}")
    return True

def main():
    """Point d'entrée principal."""
    base_path = Path(__file__).parent.parent
    translation_path = base_path / 'data' / 'strings' / 'strings.json'
    original_path = Path('D:/Fractal Softworks/Starsector/starsector-core/data/strings/strings.json')

    if not original_path.exists():
        print(f"Erreur : Fichier original non trouvé : {original_path}")
        return

    if not translation_path.exists():
        print(f"Erreur : Fichier de traduction non trouvé : {translation_path}")
        return

    print(f"Correction du fichier : {translation_path}")
    success = fix_json_structure(str(translation_path), str(original_path))
    
    if success:
        print("Correction terminée avec succès")
    else:
        print("Des erreurs sont survenues pendant la correction")

if __name__ == '__main__':
    main()

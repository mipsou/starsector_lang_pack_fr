#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

def remove_comments(content):
    """Supprime les commentaires d'un fichier JSON."""
    lines = []
    for line in content.split('\n'):
        # Ignorer les lignes de commentaires
        if line.strip().startswith('#'):
            continue
        # Supprimer les commentaires en fin de ligne
        if '#' in line:
            line = line[:line.index('#')].rstrip()
        if line.strip():
            lines.append(line)
    return '\n'.join(lines)

def fix_special_chars(text):
    """Corrige les caractères spéciaux mal encodés."""
    char_map = {
        'ééé': 'é',
        'éé': 'é',
        'ééà': 'à',
        'ééâ': 'â',
        'ééè': 'è',
        'ééê': 'ê',
        'ééë': 'ë',
        'ééî': 'î',
        'ééï': 'ï',
        'ééô': 'ô',
        'ééù': 'ù',
        'ééû': 'û',
        'ééü': 'ü',
        'ééÿ': 'ÿ',
        'ééç': 'ç',
        'éÂé': 'é',
        'âÂ': 'â',
        'éÂ': 'é',
        'ééÂ': 'é',
        'ééé': 'é',
        'éééé': 'é',
        'ééééé': 'é',
        'âÂé': 'â',
        'éÂâ': 'é',
        'ééét': 'ét',
        'ééée': 'ée',
        'ééés': 'és',
        'ééér': 'ér',
        'ééél': 'él',
        'ééég': 'ég',
        'ééép': 'ép',
        'ééém': 'ém',
        'ééév': 'év',
        'ééén': 'én',
        'ééÂé': 'é',
        'gééÂé': 'gé',
        'dééÂé': 'dé',
        'rééÂé': 'ré',
        'tééÂé': 'té',
        'mééÂé': 'mé',
        'pééÂé': 'pé',
        'lééÂé': 'lé',
        'vééÂé': 'vé',
        'nééÂé': 'né'
    }
    
    # Premier passage : correction des caractères spéciaux
    for bad, good in char_map.items():
        text = text.replace(bad, good)
    
    # Deuxième passage : suppression des caractères parasites restants
    text = text.replace('éé', 'é')
    text = text.replace('Â', '')
    
    return text

def fix_trailing_commas(content):
    """Supprime les virgules en trop dans le contenu JSON."""
    # Nettoie d'abord les sauts de ligne pour un meilleur traitement
    lines = content.split('\n')
    cleaned_lines = []
    in_string = False
    quote_char = None
    
    for line in lines:
        # Gestion des chaînes de caractères
        i = 0
        cleaned_line = ""
        while i < len(line):
            char = line[i]
            
            # Détection des guillemets
            if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None
                    
            # Si on n'est pas dans une chaîne, on nettoie les virgules
            if not in_string:
                if char == ',' and i < len(line)-1:
                    next_non_space = None
                    for j in range(i+1, len(line)):
                        if line[j] not in [' ', '\t', '\n', '\r']:
                            next_non_space = line[j]
                            break
                    if next_non_space in [']', '}', None]:
                        continue
                        
            cleaned_line += char
            i += 1
            
        cleaned_lines.append(cleaned_line)
    
    content = '\n'.join(cleaned_lines)
    
    # Supprime les virgules avant }
    content = content.replace(",}", "}")
    # Supprime les virgules avant ]
    content = content.replace(",]", "]")
    # Supprime les virgules doubles
    content = content.replace(",,", ",")
    
    return content

def validate_json_structure(content):
    """Valide et corrige la structure JSON."""
    # Vérifie les paires clé-valeur incomplètes
    lines = content.split('\n')
    valid_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Ignore les lignes de commentaires
        if line.startswith('#'):
            continue
            
        # Vérifie si la ligne est une paire clé-valeur valide
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().strip('"')
            value = value.strip()
            
            # Si la valeur est vide ou invalide, on l'ignore
            if not value or value == '{' or value == '[' or value == ']' or value == '}':
                continue
                
            # Reconstruit la ligne avec le bon format
            valid_lines.append(f'"{key}": {value}')
            
    # Reconstruit le contenu JSON
    content = "{\n" + ",\n".join(valid_lines) + "\n}"
    return content

def fix_json_structure(translation_path, original_path):
    """
    Corrige la structure JSON du fichier de traduction en se basant sur l'original.
    
    Args:
        translation_path (str): Chemin vers le fichier de traduction à corriger
        original_path (str): Chemin vers le fichier original servant de référence
    """
    try:
        # Lecture du fichier original avec détection de l'encodage
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read().strip()
            if not original_content:
                raise ValueError(f"Le fichier original {original_path} est vide")
                
            # Supprimer les commentaires avant de parser le JSON
            original_content = remove_comments(original_content)
            # Valider la structure JSON
            original_content = validate_json_structure(original_content)
            # Corriger les virgules en trop
            original_content = fix_trailing_commas(original_content)
            
            try:
                original_json = json.loads(original_content)
            except json.JSONDecodeError as e:
                print(f"Erreur dans le fichier original à la position {e.pos}, ligne {e.lineno}, colonne {e.colno}")
                print(f"Le contenu autour de l'erreur : {original_content[max(0, e.pos-50):min(len(original_content), e.pos+50)]}")
                raise
        
        # Lecture du fichier de traduction avec détection de l'encodage
        with open(translation_path, 'r', encoding='utf-8') as f:
            translation_content = f.read().strip()
            if not translation_content:
                raise ValueError(f"Le fichier de traduction {translation_path} est vide")
            
        # Correction des caractères spéciaux
        translation_content = fix_special_chars(translation_content)
        
        # Supprimer les commentaires avant de parser le JSON
        translation_content = remove_comments(translation_content)
        
        # Valider la structure JSON
        translation_content = validate_json_structure(translation_content)
        
        # Corriger les virgules en trop
        translation_content = fix_trailing_commas(translation_content)
        
        try:
            translation_json = json.loads(translation_content)
        except json.JSONDecodeError as e:
            print(f"Erreur dans le fichier de traduction à la position {e.pos}, ligne {e.lineno}, colonne {e.colno}")
            print(f"Le contenu autour de l'erreur : {translation_content[max(0, e.pos-50):min(len(translation_content), e.pos+50)]}")
            raise
            
        # Vérification et correction de la structure
        corrected_json = {}
        for key in original_json:
            if key in translation_json:
                corrected_json[key] = translation_json[key]
            else:
                corrected_json[key] = original_json[key]
                print(f"Clé manquante dans la traduction : {key}, utilisation de la version originale")
                
        # Écriture du fichier corrigé
        with open(translation_path, 'w', encoding='utf-8') as f:
            json.dump(corrected_json, f, ensure_ascii=False, indent=4)
            
        print(f"Structure JSON corrigée avec succès pour {translation_path}")
        
    except Exception as e:
        print(f"Erreur lors de la correction de la structure JSON : {str(e)}")
        raise

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python json_utils.py <translation_file> <original_file>")
        sys.exit(1)
    
    translation_path = sys.argv[1]
    original_path = sys.argv[2]
    fix_json_structure(translation_path, original_path)

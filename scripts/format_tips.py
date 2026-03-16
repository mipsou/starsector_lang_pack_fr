#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de formatage des fichiers tips.json pour Starsector.
Respecte les conventions de formatage spécifiques au jeu.

Format attendu :
- Pas d'espace après les deux points dans les clés
- Guillemets droits (") uniquement
- Indentation de 4 espaces exactement
- Sauts de ligne style Unix (\n)

Auteur: Mipsou
Date: 2025-01-22
"""

import re
import json
import sys
from utils import format_starsector_json, fix_quotes

def parse_tips(content):
    """Parse le contenu du fichier tips.json.
    
    Args:
        content (str): Contenu du fichier
        
    Returns:
        list: Liste des tips
    """
    tips = []
    
    # Extraire le contenu entre les crochets
    if match := re.search(r'{\s*tips\s*:\s*\[(.*?)\]\s*}', content, re.DOTALL):
        tips_content = match.group(1)
        current = ""
        in_string = False
        in_object = False
        escape = False
        depth = 0
        
        for char in tips_content:
            if escape:
                current += char
                escape = False
                continue
                
            if char == '\\':
                current += char
                escape = True
                continue
                
            if char == '"' and not escape:
                in_string = not in_string
                
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    
            current += char
            
            if char == ',' and depth == 0 and not in_string:
                tip = current.strip().rstrip(',')
                if tip:
                    tips.append(tip)
                current = ""
                continue
                
        if current.strip():
            tip = current.strip().rstrip(',')
            if tip:
                tips.append(tip)
                
    return tips

def format_tips_file(file_path):
    """Formate un fichier tips.json.
    
    Args:
        file_path (str): Chemin du fichier
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Parser les tips
    tips = parse_tips(content)
    if not tips:
        print("Aucun tip trouvé")
        return
        
    # Nettoyer et normaliser les tips
    formatted_tips = []
    for tip in tips:
        if tip.startswith('{'):
            # C'est un objet JSON
            try:
                obj = json.loads(tip)
                if 'freq' in obj and 'tip' in obj:
                    obj['tip'] = fix_quotes(obj['tip'])
                    formatted_tips.append(json.dumps(obj, ensure_ascii=False))
            except:
                print(f"Erreur avec l'objet: {tip}")
        else:
            # C'est une chaîne simple
            tip = tip.strip('"')
            tip = fix_quotes(tip)
            formatted_tips.append(f'"{tip}"')
            
    # Créer le dictionnaire final
    data = {"tips": formatted_tips}
    
    # Formater et sauvegarder
    formatted = format_starsector_json(data)
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(formatted)
        
    print(f"Formaté {len(formatted_tips)} tips")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python format_tips.py <file_path>")
        sys.exit(1)
    format_tips_file(sys.argv[1])

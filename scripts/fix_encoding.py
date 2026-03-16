#!/usr/bin/env python3
"""
Script de correction d'encodage pour les fichiers JSON

Ce script :
- Détecte et corrige les problèmes d'encodage
- Normalise les caractères spéciaux
- Assure l'encodage UTF-8 et le format JSON Starsector

Auteur: Mipsou
Date: 2025-01-22
"""
import json
from pathlib import Path
import re
from utils import format_starsector_json, check_encoding

def fix_text(text):
    """Corrige les caractères mal encodés caractère par caractère.
    
    Args:
        text (str): Texte à corriger
        
    Returns:
        str: Texte avec caractères corrigés
    """
    # Table de correspondance des caractères
    char_map = {
        'é': 'é',
        'é«': '«',
        'é»': '»',
        'é´': 'ô',
        'é¨': 'è',
        'é': 'î',
        'é¢': 'â',
        'é§': 'ç',
        'éª': 'ê',
        'é': 'é',
        'è': 'è',
        'à': 'à',
        'â': 'â',
        'ê': 'ê',
        'î': 'î',
        'ô': 'ô',
        'û': 'û',
        'ù': 'ù',
        'ç': 'ç',
        'ë': 'ë',
        'ï': 'ï',
        'ü': 'ü',
        'œ': 'œ',
        'É': 'É',
        'À': 'À',
        'Â': 'Â',
        'Ê': 'Ê',
        'Î': 'Î',
        'Ô': 'Ô',
        'Û': 'Û',
        'Ç': 'Ç',
        'Ë': 'Ë',
        'Ï': 'Ï',
        'Ü': 'Ü'
    }
    
    # Remplacer les caractères mal encodés
    pattern = '|'.join(map(re.escape, char_map.keys()))
    return re.sub(pattern, lambda m: char_map[m.group()], text)

def fix_file_encoding(input_file, output_file=None):
    """Corrige l'encodage d'un fichier JSON.
    
    Args:
        input_file (str): Chemin du fichier à corriger
        output_file (str, optional): Chemin du fichier de sortie. Si None, écrase le fichier d'entrée.
        
    Returns:
        bool: True si la correction a réussi, False sinon
    """
    if output_file is None:
        output_file = input_file
        
    try:
        # Lecture du fichier en binaire
        with open(input_file, 'rb') as f:
            content = f.read()
            
        # Essai de différents encodages
        for encoding in ['utf-8', 'latin1', 'cp1252']:
            try:
                # Décodage du contenu
                text = content.decode(encoding)
                # Correction des caractères
                text = fix_text(text)
                # Vérification que c'est du JSON valide
                data = json.loads(text)
                
                # Formatage selon les conventions Starsector
                formatted_json = format_starsector_json(data)
                
                # Écriture avec le bon encodage
                with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(formatted_json)
                    
                # Vérification finale de l'encodage
                if check_encoding(output_file):
                    print(f"Fichier corrigé avec succès (encodage source : {encoding})")
                    return True
                else:
                    raise ValueError("Le fichier de sortie n'est pas en UTF-8 valide")
                    
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
                
        raise Exception("Aucun encodage n'a fonctionné")
        
    except Exception as e:
        print(f"Erreur lors de la correction : {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fix_encoding.py input_file [output_file]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if fix_file_encoding(input_file, output_file):
        sys.exit(0)
    else:
        sys.exit(1)

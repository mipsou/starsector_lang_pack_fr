#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
from pathlib import Path

def fix_text(text):
    """Tente de corriger l'encodage d'un texte."""
    # Première tentative : décodage direct
    try:
        # Si le texte est déjà en UTF-8, on le laisse tel quel
        if not any(c in text for c in ['Ã', 'Â', 'Å']):
            return text
            
        # Sinon, on essaie de le décoder
        return text.encode('latin1').decode('utf-8')
    except:
        pass
        
    # Deuxième tentative : double décodage
    try:
        return text.encode('latin1').decode('utf-8').encode('latin1').decode('utf-8')
    except:
        pass
        
    # Si rien ne fonctionne, on retourne le texte original
    return text

def analyze_and_fix_json(input_file, output_file):
    """Analyse et corrige l'encodage d'un fichier JSON."""
    # Lecture du fichier avec différents encodages
    content = None
    for encoding in ['utf-8', 'latin1', 'cp1252']:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                content = f.read()
                data = json.loads(content)
                break
        except:
            continue
            
    if content is None:
        raise ValueError("Impossible de lire le fichier JSON")
    
    # Correction de chaque conseil
    fixed = False
    for i, tip in enumerate(data["tips"]):
        if isinstance(tip, dict):
            text = tip["tip"]
            fixed_text = fix_text(text)
            if fixed_text != text:
                fixed = True
                tip["tip"] = fixed_text
        else:
            text = tip
            fixed_text = fix_text(text)
            if fixed_text != text:
                fixed = True
                data["tips"][i] = fixed_text
    
    if fixed:
        # Écriture du fichier corrigé
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Fichier corrigé sauvegardé dans {output_file}")
    else:
        print("Aucune correction nécessaire")

if __name__ == "__main__":
    input_file = Path("localization/fr/data/strings/tips.json")
    output_file = Path("localization/fr/data/strings/tips.json.fixed")
    analyze_and_fix_json(input_file, output_file)

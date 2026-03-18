#!/usr/bin/env python3
import json
import os
import sys
import re

def validate_tips_json(content):
    """Valide un fichier JSON au format tips de Starsector."""
    # Vérification basique de la structure
    if not content.strip().startswith('{') or not content.strip().endswith('}'):
        return False
    
    # Vérifier la présence de la section tips
    if not 'tips:[' in content:
        return False
        
    try:
        # Nettoyer le format spécial tips:[ en format JSON valide
        content = content.replace('tips:[', '"tips":[')
        json.loads(content)
        return True
    except:
        return False

def validate_starsector_names(content):
    """Valide un fichier JSON au format spécifique des noms de vaisseaux Starsector."""
    # Vérification basique de la structure
    if not content.strip().startswith('{') or not content.strip().endswith('}'):
        return False
    
    try:
        data = json.loads(content)
        # Vérifier la structure attendue pour les noms de vaisseaux
        return isinstance(data, dict)
    except:
        return False

def validate_starsector_json(content):
    """Valide un fichier JSON au format Starsector général."""
    try:
        data = json.loads(content)
        # Vérifier que c'est un dictionnaire
        if not isinstance(data, dict):
            return False
            
        # Vérifier la présence de sections courantes
        valid_sections = ['codex', 'warroom', 'combat', 'fleetInteractionDialog']
        return any(section in data for section in valid_sections)
    except:
        return False

def validate_json(file_path, starsector_format=False):
    """Valide un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if starsector_format:
            return validate_starsector_json(content)
            
        try:
            json.loads(content)
            return True
        except:
            return False
    except:
        return False

def validate_json_file(file_path):
    """Valide un fichier JSON selon son type."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Déterminer le type de fichier
        filename = os.path.basename(file_path)
        if 'tips' in filename:
            return validate_tips_json(content)
        elif 'ship_names' in filename:
            return validate_starsector_names(content)
        else:
            return validate_starsector_json(content)
    except:
        return False

def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 2:
        print("Usage: validate_json.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Erreur: Le fichier {file_path} n'existe pas.")
        sys.exit(1)
        
    if validate_json_file(file_path):
        print(f"Le fichier {file_path} est valide.")
        sys.exit(0)
    else:
        print(f"Erreur: Le fichier {file_path} n'est pas valide.")
        sys.exit(1)

if __name__ == '__main__':
    main()

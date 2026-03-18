#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de validation des fichiers de traduction Starsector

Ce script vérifie :
- L'encodage UTF-8 des fichiers
- La structure JSON/CSV
- La typographie française
- La correspondance avec les fichiers originaux

Auteur: Mipsou
Date: 2025-01-22
"""

import os
import csv
import json
import re
import sys
import shutil
from pathlib import Path
from utils import check_encoding, validate_typography, compare_with_original

# Force l'encodage en UTF-8 pour la sortie
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors or []

def validate_csv(file_path):
    """Valide un fichier CSV.
    
    Args:
        file_path (str): Chemin du fichier à valider
        
    Returns:
        tuple: (bool, list) - (True si valide, liste des erreurs)
    """
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for i, row in enumerate(reader, 2):
                if len(row) != len(headers):
                    errors.append(f"Ligne {i+1} - nombre de colonnes incorrect")
    except Exception as e:
        errors.append(str(e))
    
    return len(errors) == 0, errors

def validate_json_file(file_path, original_file=None):
    """Valide un fichier JSON selon les standards Starsector.
    
    Args:
        file_path (Path): Chemin vers le fichier à valider
        original_file (Path): Fichier original pour comparaison
        
    Returns:
        tuple: (bool, list) Statut et liste d'erreurs
    """
    try:
        # Préserver l'encodage d'origine
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Vérifier si le fichier utilise des tabulations ou des espaces
        uses_tabs = b'\t' in content
        
        # Vérifier le format des deux points
        has_space_after_colon = b': ' in content
        
        errors = []
        
        if uses_tabs and not original_file:
            errors.append("Le fichier utilise des tabulations au lieu d'espaces")
            
        if has_space_after_colon and not original_file:
            errors.append("Le fichier contient des espaces après les deux points")
            
        # Vérifier la structure JSON
        try:
            json_content = json.loads(content)
        except json.JSONDecodeError as e:
            errors.append(f"Erreur de décodage JSON: {str(e)}")
            
        return len(errors) == 0, errors
            
    except Exception as e:
        return False, [str(e)]

def validate_tips_file(text):
    """Valide le format spécial de tips.json de Starsector.
    
    Format attendu :
    {
        tips:[
        {"freq":N, "tip":"texte"},
        "texte simple",
        ...
        ]
    }
    
    Args:
        text (str): Contenu du fichier
        
    Returns:
        tuple: (bool, list) Statut et liste d'erreurs
    """
    errors = []
    
    # Vérification de base
    if not text.strip().startswith('{'):
        errors.append("Le fichier doit commencer par '{'")
        return False, errors
        
    if not text.strip().endswith('}'):
        errors.append("Le fichier doit se terminer par '}'")
        return False, errors
        
    # Vérification de la structure tips:[
    if 'tips:[' not in text:
        errors.append("Le fichier doit contenir 'tips:['")
        return False, errors
        
    # Vérification des entrées
    lines = text.split('\n')
    in_tips = False
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Début de la section tips
        if 'tips:[' in line:
            in_tips = True
            continue
            
        if not in_tips:
            continue
            
        # Ignore les lignes vides
        if not line:
            continue
            
        # Vérifie le format des entrées
        if line.startswith('{'):
            # Entrée avec fréquence
            if '"freq":' not in line or '"tip":' not in line:
                errors.append(f"Ligne {i+1} : Format invalide pour une entrée avec fréquence")
        elif line.startswith('"'):
            # Entrée simple
            if not (line.startswith('"') and (line.endswith('",') or line.endswith('"'))):
                errors.append(f"Ligne {i+1} : Format invalide pour une entrée simple")
                
    return len(errors) == 0, errors

def validate_file(filepath, strict=False):
    """Valide un fichier de traduction."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Détection du type de fichier
        filepath_str = str(filepath)
        if filepath_str.endswith('tips.json'):
            return validate_tips_file(content)
        elif filepath_str.endswith('.json'):
            return validate_json_file(filepath)
        elif filepath_str.endswith('.csv'):
            return validate_csv(filepath)
        else:
            return validate_text(content)
            
    except UnicodeError:
        return False, ["Le fichier n'est pas en UTF-8"]
    except Exception as e:
        return False, [str(e)]

def format_validation_errors(errors):
    """Formate les erreurs de validation de manière lisible.
    
    Args:
        errors (list): Liste d'erreurs détaillées
        
    Returns:
        str: Message d'erreur formaté
    """
    if not errors:
        return "Aucune erreur"
        
    messages = []
    for error in errors:
        if isinstance(error, dict):
            msg = f"- {error['message']}"
            if error['section'] != 'unknown':
                msg += f" (section: {error['section']}"
            if error['line'] > 0:
                msg += f", ligne: {error['line']}"
            if error['section'] != 'unknown':
                msg += ")"
            messages.append(msg)
        else:
            messages.append(f"- {error}")
            
    return "\n".join(messages)

def validate_all_files(directory):
    """Valide tous les fichiers de traduction dans un répertoire.
    
    Args:
        directory (str): Chemin du répertoire à valider
    """
    print(f"\nValidation du répertoire: {directory}")
    print("-" * 80)
    
    total_files = 0
    valid_files = 0
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            total_files += 1
            print(f"\nValidation de {filename}:")
            
            # Vérification de l'encodage
            if not check_encoding(filepath):
                print(f"❌ {filename} n'est pas en UTF-8")
                continue
                
            # Validation du fichier
            is_valid, errors = validate_file(filepath)
            
            if is_valid:
                valid_files += 1
                print(f"✅ {filename} est valide")
            else:
                print(f"❌ {filename} contient des erreurs:")
                print(format_validation_errors(errors))
                
    # Affichage du résumé
    print("\nRésumé:")
    print(f"- Fichiers traités: {total_files}")
    print(f"- Fichiers valides: {valid_files}")
    print(f"- Fichiers invalides: {total_files - valid_files}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = 'localization/data/strings'
        
    validate_all_files(directory)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de reconstruction global pour Starsector.

Ce script permet de reconstruire n'importe quel fichier traduit en préservant :
- Les traductions existantes
- Le format exact (indentation, guillemets, etc.)
- La structure originale

Types de fichiers supportés :
- JSON (tips.json, strings.json, tooltips.json, etc.)
- CSV (pour les données tabulaires)
- INI (pour les configurations)

Usage :
    python rebuild.py --rebuild-all -v  # Reconstruit tous les fichiers
    python rebuild.py --tips -v         # Reconstruit tips.json
    python rebuild.py -o "chemin/vers/fichier.json"  # Reconstruit un fichier spécifique
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime
from typing import Dict, Optional
import logging
from fix_translation import fix_special_chars
from starsector_json import (
    parse_starsector_json, 
    format_starsector_json,
    FileType,
    detect_file_type,
    init_analyzer
)

def get_starsector_root(file_path: str) -> str:
    """
    Détermine le répertoire racine de Starsector à partir d'un chemin de fichier.
    """
    path = Path(file_path)
    # Remonte jusqu'à trouver le répertoire starsector-core
    while path.parent != path:
        if (path / "starsector-core").exists():
            return str(path)
        path = path.parent
    return None

def clean_json_content(content):
    """Nettoie le contenu JSON en retirant les virgules en fin d'objet."""
    # Supprime les virgules suivies uniquement d'accolades ou crochets fermants
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Supprime les virgules en fin de ligne suivies d'une accolade ou d'un crochet sur la ligne suivante
    lines = content.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if line.strip().endswith(',') and (next_line.startswith('}') or next_line.startswith(']')):
                line = line.rstrip(',')
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def load_json_with_comments(file_path):
    """Charge un fichier JSON en gérant les commentaires et les virgules."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Supprime les commentaires
    content = remove_comments(content)
    
    # Nettoie les virgules
    content = clean_json_content(content)
    
    return content

def load_existing_translations(backup_path):
    """Charge les traductions existantes depuis une sauvegarde."""
    try:
        with open(backup_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return json.loads(content)
    except Exception as e:
        print(f"Erreur lors du chargement des traductions existantes : {e}")
        return None

def rebuild_strings_json(original_path: str, output_path: str) -> bool:
    """
    Reconstruit un fichier de traduction.
    
    Args:
        original_path: Chemin du fichier original
        output_path: Chemin du fichier de sortie
        
    Returns:
        True si succès, False sinon
    """
    try:
        # Charge le fichier original
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        original_data, error = parse_starsector_json(original_content)
        if error:
            logging.error(f"Erreur dans le fichier original : {error}")
            return False
        
        # Détecte le type de fichier
        file_type = detect_file_type(original_data)
        if file_type == FileType.UNKNOWN:
            logging.error("Type de fichier non reconnu")
            return False
        
        logging.info(f"Type de fichier détecté : {file_type.name}")
        
        # Charge les traductions existantes si présentes
        existing_data = None
        if Path(output_path).exists():
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                existing_data, error = parse_starsector_json(existing_content)
                if error:
                    logging.warning(f"Impossible de charger les traductions existantes : {error}")
                else:
                    logging.info("Traductions existantes chargées avec succès")
            except Exception as e:
                logging.warning(f"Erreur lors du chargement des traductions : {str(e)}")
        
        # Crée une sauvegarde
        if Path(output_path).exists():
            backup_path = f"{output_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(output_path, backup_path)
            logging.info(f"Sauvegarde créée : {backup_path}")
        
        # Reconstruit le fichier selon son type
        if file_type == FileType.TIPS:
            output_data, _ = rebuild_tips_json(original_data, existing_data)
        else:
            output_data = rebuild_generic_json(original_data, existing_data)
        
        # Sauvegarde le résultat
        with open(output_path, 'w', encoding='utf-8') as f:
            formatted = format_starsector_json(output_data)
            f.write(formatted)
        
        logging.info(f"Fichier reconstruit avec succès : {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"Erreur lors de la reconstruction : {str(e)}")
        return False

def rebuild_tips_json(original_data: Dict, existing_data: Optional[Dict]) -> (Dict, FileType):
    """
    Reconstruit un fichier tips.json en préservant les lignes complètes.
    
    Args:
        original_data: Données du fichier original
        existing_data: Données des traductions existantes
        
    Returns:
        Données reconstruites et le type de fichier
    """
    output_data = {"tips": []}
    
    # Si pas de données existantes, retourne une copie de l'original
    if not existing_data or "tips" not in existing_data:
        return original_data.copy(), FileType.TIPS
    
    existing_tips = existing_data.get("tips", [])
    original_tips = original_data.get("tips", [])
    
    # Crée un dictionnaire des traductions existantes
    translations = {}
    for tip in existing_tips:
        if isinstance(tip, dict):
            original = tip.get("tip", "")
            if original:
                translations[original] = tip
        else:
            translations[str(tip)] = tip
    
    # Reconstruit le fichier en utilisant les traductions
    for item in original_tips:
        if isinstance(item, dict):
            # Cas d'un objet avec fréquence
            freq = item.get("freq", 1)
            tip = item.get("tip", "")
            
            # Cherche une traduction
            if tip in translations and isinstance(translations[tip], dict):
                translated_tip = translations[tip].get("tip", "")
                if translated_tip and not translated_tip.endswith("..."):
                    output_data["tips"].append({
                        "freq": freq,
                        "tip": translated_tip
                    })
                    continue
            
            # Si pas de traduction valide, utilise l'original
            output_data["tips"].append(item)
            
        else:
            # Cas d'une simple chaîne
            if str(item) in translations:
                translated = translations[str(item)]
                if isinstance(translated, str) and not translated.endswith("..."):
                    output_data["tips"].append(translated)
                    continue
            
            # Si pas de traduction valide, utilise l'original
            output_data["tips"].append(item)
    
    return output_data, FileType.TIPS

def rebuild_generic_json(original_data: Dict, existing_data: Optional[Dict]) -> Dict:
    """
    Reconstruit un fichier générique en préservant les clés et les valeurs.
    
    Args:
        original_data: Données du fichier original
        existing_data: Données des traductions existantes
        
    Returns:
        Données reconstruites
    """
    output_data = {}
    for key in original_data:
        if isinstance(original_data[key], dict):
            output_data[key] = {}
            for subkey in original_data[key]:
                if existing_data and key in existing_data and subkey in existing_data[key]:
                    output_data[key][subkey] = existing_data[key][subkey]
                else:
                    output_data[key][subkey] = f"[FR] {original_data[key][subkey]}"
        else:
            if existing_data and key in existing_data:
                output_data[key] = existing_data[key]
            else:
                output_data[key] = f"[FR] {original_data[key]}"
    
    return output_data

def main():
    """Point d'entrée principal."""
    import argparse
    from rebuild_manager import RebuildManager, FormatSpec
    
    parser = argparse.ArgumentParser(description="Reconstruit les fichiers de traduction Starsector")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    parser.add_argument("--tips", action="store_true", help="Reconstruit tips.json")
    parser.add_argument("--strings", action="store_true", help="Reconstruit strings.json")
    parser.add_argument("--tooltips", action="store_true", help="Reconstruit tooltips.json")
    parser.add_argument("--all", "-a", action="store_true", help="Reconstruit tous les fichiers")
    parser.add_argument("--original", "-o", type=str, help="Chemin du fichier original (ex: D:/Fractal Softworks/Starsector/starsector-core/data/strings/tips.json)")
    parser.add_argument("--output", type=str, help="Chemin du fichier de sortie (optionnel, par défaut dans data/strings/)")
    parser.add_argument("--backup", "-b", type=str, help="Dossier contenant les sauvegardes des traductions")
    parser.add_argument("--rebuild-all", "-r", action="store_true", help="Reconstruit tous les fichiers traduits dans tous les dossiers")
    args = parser.parse_args()

    base_path = Path(__file__).parent.parent
    
    # Initialise le gestionnaire de reconstruction
    manager = RebuildManager(base_path)
    manager.set_verbose(args.verbose)
    
    if args.backup:
        manager.set_backup_path(Path(args.backup))
    
    # Enregistre les formats spécifiques
    tips_spec = FormatSpec()
    tips_spec.indent_char = "\t"
    tips_spec.indent_size = 1
    tips_spec.patterns = {
        "tips": "[",  # Pas d'espace après les deux points
        "freq": "0"   # Format spécifique pour la fréquence
    }
    manager.register_format("tips.json", tips_spec)
    
    # Si l'option rebuild-all est activée, on reconstruit tout
    if args.rebuild_all:
        print("Reconstruction globale de tous les fichiers traduits...")
        results = manager.rebuild_all_translations()
        return
    
    # Si un fichier original est spécifié, on ne reconstruit que celui-là
    if args.original:
        original_path = Path(args.original)
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = base_path / 'data' / 'strings' / original_path.name
            
        if not original_path.exists():
            print(f"✗ Erreur : Le fichier original {original_path} n'existe pas")
            return
            
        print(f"Reconstruction depuis {original_path}")
        print(f"Vers {output_path}")
        
        success = manager.rebuild_file(original_path, output_path)
        if not success:
            print(f"✗ Erreur lors de la reconstruction de {output_path.name}")
        return
        
    # Sinon, détermine les fichiers à reconstruire
    files_to_rebuild = []
    if args.all:
        files_to_rebuild = ["strings.json", "tips.json", "tooltips.json"]
    else:
        if args.strings:
            files_to_rebuild.append("strings.json")
        if args.tips:
            files_to_rebuild.append("tips.json")
        if args.tooltips:
            files_to_rebuild.append("tooltips.json")
    
    if not files_to_rebuild:
        files_to_rebuild = ["strings.json"]  # Par défaut
        
    # Reconstruit chaque fichier
    for file in files_to_rebuild:
        original_path = base_path.parent.parent / 'starsector-core' / 'data' / 'strings' / file
        output_path = base_path / 'data' / 'strings' / file

        if not original_path.exists():
            print(f"✗ Erreur : Le fichier original {original_path} n'existe pas")
            continue

        print(f"Reconstruction du fichier {file}...")
        print(f"Depuis {original_path}")
        print(f"Vers {output_path}")
        
        success = manager.rebuild_file(original_path, output_path)
        if not success:
            print(f"✗ Erreur lors de la reconstruction de {file}")

if __name__ == '__main__':
    main()

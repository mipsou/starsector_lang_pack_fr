#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de gestion des traductions pour Starsector
================================================

Format spécifique du jeu :
- Fichiers JSON avec indentation de 4 espaces
- Pas d'espace après les deux points dans les clés
- Guillemets droits (") uniquement
- Encodage UTF-8 obligatoire et non négociable

Fonctions principales :
- rebuild : Reconstruction d'un fichier de traduction
- validate : Validation de la structure et du format
- fix : Correction automatique des erreurs courantes

Tests systématiques :
- Validation de l'encodage UTF-8
- Vérification de la structure JSON
- Comparaison avec le fichier original
- Test des guillemets et apostrophes

Gestion des erreurs :
- Capture et log de toutes les exceptions
- Messages d'erreur explicites
- Validation des fichiers d'entrée/sortie
"""

import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple
from datetime import datetime

from starsector_json import (
    init_analyzer,
    FileType,
    parse_starsector_json,
    detect_file_type
)
from rebuild_strings import rebuild_strings_json
from fix_translation import fix_special_chars

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationResult:
    """Résultat d'une validation de traduction."""
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def add_error(self, message: str):
        """Ajoute une erreur avec logging."""
        self.errors.append(message)
        logger.error(message)
        
    def add_warning(self, message: str):
        """Ajoute un avertissement avec logging."""
        self.warnings.append(message)
        logger.warning(message)
        
    @property
    def is_valid(self) -> bool:
        """Vérifie si la validation est réussie."""
        return len(self.errors) == 0
        
    def __str__(self) -> str:
        """Formate le résultat pour l'affichage."""
        result = []
        if self.errors:
            result.append("Erreurs :")
            for error in self.errors:
                result.append(f"  ✗ {error}")
        if self.warnings:
            result.append("Avertissements :")
            for warning in self.warnings:
                result.append(f"  ! {warning}")
        return "\n".join(result) if result else "Aucun problème détecté"

def validate_translation(file_path: Path, original_path: Path) -> ValidationResult:
    """
    Valide un fichier de traduction selon les spécifications Starsector.
    
    Vérifie :
    - Encodage UTF-8
    - Structure JSON valide
    - Format spécifique (indentation, espaces)
    - Correspondance avec la structure originale
    - Variables système préservées
    - Caractères spéciaux valides
    
    Args:
        file_path: Chemin vers le fichier de traduction
        original_path: Chemin vers le fichier original
        
    Returns:
        ValidationResult contenant les erreurs et avertissements
    """
    result = ValidationResult()
    logger.info(f"Validation de {file_path}")
    
    # Test d'encodage UTF-8
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translation_content = f.read()
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except UnicodeDecodeError as e:
        result.add_error(f"Erreur d'encodage UTF-8 : {str(e)}")
        return result
    except Exception as e:
        result.add_error(f"Erreur de lecture : {str(e)}")
        return result
        
    # Parse et validation JSON
    original_data, original_error = parse_starsector_json(original_content)
    if original_error:
        result.add_error(f"Erreur dans le fichier original : {original_error}")
        return result
        
    translation_data, translation_error = parse_starsector_json(translation_content)
    if translation_error:
        result.add_error(f"Erreur dans la traduction : {translation_error}")
        return result
        
    # Vérification du format spécifique
    _validate_format(translation_content, result)
    
    # Vérification de la structure
    original_type = detect_file_type(original_data)
    translation_type = detect_file_type(translation_data)
    
    if original_type != translation_type:
        result.add_error(f"Type de fichier différent : {original_type.name} vs {translation_type.name}")
        return result
        
    # Validation spécifique selon le type
    if original_type == FileType.TIPS:
        _validate_tips(original_data, translation_data, result)
    elif original_type == FileType.TOOLTIPS:
        _validate_tooltips(original_data, translation_data, result)
    else:  # STRINGS
        _validate_strings(original_data, translation_data, result)
        
    # Vérification des caractères spéciaux
    _validate_special_chars(translation_content, result)
    
    return result

def _validate_format(content: str, result: ValidationResult):
    """Valide le format spécifique de Starsector."""
    # Vérifie l'indentation
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if line.strip():
            indent = len(line) - len(line.lstrip())
            if indent > 0 and indent % 4 != 0:
                result.add_error(f"Ligne {i} : indentation incorrecte (doit être multiple de 4)")
                
    # Vérifie les espaces après les deux points
    for i, line in enumerate(lines, 1):
        if '": ' in line:
            result.add_error(f"Ligne {i} : espace après les deux points dans une clé")

def _validate_tips(original: List, translation: List, result: ValidationResult):
    """Valide un fichier tips.json."""
    if len(original) != len(translation):
        result.add_error(f"Nombre d'entrées différent : {len(original)} vs {len(translation)}")
        return
        
    for i, (orig, trans) in enumerate(zip(original, translation)):
        if isinstance(orig, dict) and isinstance(trans, dict):
            if 'text' not in trans:
                result.add_error(f"Entrée {i} : champ 'text' manquant")
            elif not isinstance(trans['text'], str):
                result.add_error(f"Entrée {i} : 'text' doit être une chaîne")
        elif isinstance(orig, str) and not isinstance(trans, str):
            result.add_error(f"Entrée {i} : type incorrect")

def _validate_tooltips(original: dict, translation: dict, result: ValidationResult):
    """Valide un fichier tooltips.json."""
    for key in original:
        if key not in translation:
            result.add_error(f"Section manquante : {key}")
            continue
            
        orig_section = original[key]
        trans_section = translation[key]
        
        if isinstance(orig_section, dict):
            if not isinstance(trans_section, dict):
                result.add_error(f"Section {key} : type incorrect")
                continue
                
            if 'title' in orig_section and 'title' not in trans_section:
                result.add_error(f"Section {key} : titre manquant")
            if 'body' in orig_section and 'body' not in trans_section:
                result.add_error(f"Section {key} : corps manquant")

def _validate_strings(original: dict, translation: dict, result: ValidationResult):
    """Valide un fichier strings.json."""
    def extract_vars(text: str) -> set:
        """Extrait les variables système d'un texte."""
        import re
        return set(re.findall(r'\$\w+', text))
    
    for key in original:
        if key not in translation:
            result.add_error(f"Clé manquante : {key}")
            continue
            
        orig_value = original[key]
        trans_value = translation[key]
        
        if isinstance(orig_value, dict):
            if not isinstance(trans_value, dict):
                result.add_error(f"Section {key} : type incorrect")
                continue
                
            for subkey in orig_value:
                if subkey not in trans_value:
                    result.add_error(f"Sous-clé manquante : {key}.{subkey}")
                    continue
                    
                # Vérifie les variables système
                orig_vars = extract_vars(orig_value[subkey])
                trans_vars = extract_vars(trans_value[subkey])
                
                missing_vars = orig_vars - trans_vars
                if missing_vars:
                    result.add_error(f"{key}.{subkey} : variables manquantes : {', '.join(missing_vars)}")
                    
                extra_vars = trans_vars - orig_vars
                if extra_vars:
                    result.add_warning(f"{key}.{subkey} : variables supplémentaires : {', '.join(extra_vars)}")
        
        elif isinstance(orig_value, str):
            if not isinstance(trans_value, str):
                result.add_error(f"Clé {key} : type incorrect")
                continue
                
            # Vérifie les variables système
            orig_vars = extract_vars(orig_value)
            trans_vars = extract_vars(trans_value)
            
            missing_vars = orig_vars - trans_vars
            if missing_vars:
                result.add_error(f"{key} : variables manquantes : {', '.join(missing_vars)}")
                
            extra_vars = trans_vars - orig_vars
            if extra_vars:
                result.add_warning(f"{key} : variables supplémentaires : {', '.join(extra_vars)}")

def _validate_special_chars(content: str, result: ValidationResult):
    """Valide les caractères spéciaux selon les spécifications."""
    # Vérifie les guillemets
    if '"' in content or '"' in content or '"' in content:
        result.add_error("Guillemets courbes détectés (utilisez des guillemets droits)")
        
    # Vérifie les apostrophes
    if ''' in content or ''' in content:
        result.add_error("Apostrophes courbes détectées (utilisez des apostrophes droites)")

def setup_logging():
    """Configure le logging dans un fichier."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f"translate_{timestamp}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    return log_file

def find_json_files(data_dir: Path) -> List[Path]:
    """Trouve tous les fichiers JSON dans le répertoire data/strings."""
    strings_dir = data_dir / "strings"
    if not strings_dir.exists():
        logger.error(f"Répertoire {strings_dir} introuvable")
        return []
        
    return list(strings_dir.glob("*.json"))

def get_original_path(file_path: Path, starsector_core: Path) -> Optional[Path]:
    """Trouve le chemin du fichier original correspondant."""
    rel_path = file_path.relative_to(file_path.parent.parent.parent)
    original_path = starsector_core / rel_path
    
    if not original_path.exists():
        logger.warning(f"Fichier original introuvable : {original_path}")
        return None
        
    return original_path

def main():
    """Point d'entrée principal du script."""
    try:
        # Configure l'encodage de la console
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        
        # Configure le logging
        log_file = setup_logging()
        logger.info("Démarrage de la session de traduction")
        print(f"Les logs seront écrits dans : {log_file}")
        
        # Parse les arguments
        parser = argparse.ArgumentParser(
            description="Gestion des traductions Starsector",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__doc__
        )
        parser.add_argument('action', choices=['rebuild', 'validate', 'fix'],
                          help="Action à effectuer")
        parser.add_argument('--file', help="Fichier spécifique à traiter")
        parser.add_argument('--original', help="Chemin vers le fichier original")
        
        args = parser.parse_args()
        
        # Trouve le répertoire starsector-core
        current_dir = Path(__file__).resolve().parent
        starsector_core = None
        
        # Remonte jusqu'à trouver starsector-core
        search_dir = current_dir
        while search_dir.parent != search_dir:
            if (search_dir / "starsector-core").exists():
                starsector_core = search_dir / "starsector-core"
                break
            search_dir = search_dir.parent
        
        if not starsector_core:
            logger.error("Impossible de trouver le répertoire starsector-core")
            sys.exit(1)
        
        logger.info(f"Répertoire starsector-core trouvé : {starsector_core}")
        print(f"Répertoire starsector-core trouvé : {starsector_core}")
        
        # Initialise l'analyseur
        init_analyzer(str(starsector_core.parent))
        
        # Trouve les fichiers à traiter
        if args.file:
            files = [Path(args.file)]
        else:
            # Cherche dans le répertoire data du mod
            mod_data = current_dir.parent / "data"
            files = find_json_files(mod_data)
        
        if not files:
            logger.error("Aucun fichier à traiter")
            sys.exit(1)
        
        # Traite chaque fichier
        for file_path in files:
            logger.info(f"Traitement de {file_path}")
            print(f"\nTraitement de {file_path}")
            
            # Trouve le fichier original correspondant
            original = None
            if args.original:
                original = Path(args.original)
            else:
                original = get_original_path(file_path, starsector_core)
                
            if not original:
                continue
                
            if args.action == 'rebuild':
                logger.info(f"Reconstruction de {file_path}")
                if rebuild_strings_json(str(original), str(file_path)):
                    logger.info(f"Fichier reconstruit avec succès : {file_path}")
                    print(f"✓ Fichier reconstruit avec succès : {file_path}")
                else:
                    logger.error(f"Erreur lors de la reconstruction de {file_path}")
                    print(f"✗ Erreur lors de la reconstruction de {file_path}")
                    
            elif args.action == 'validate':
                logger.info(f"Validation de {file_path}")
                result = validate_translation(file_path, original)
                if result.is_valid:
                    logger.info(f"Validation réussie : {file_path}")
                    print(f"✓ Validation réussie : {file_path}")
                else:
                    logger.error(f"Validation échouée : {file_path}")
                    print(f"✗ Validation échouée : {file_path}")
                print(str(result))
                
            elif args.action == 'fix':
                logger.info(f"Correction de {file_path}")
                # TODO: Implémenter la correction
                print("Correction non implémentée")

    except Exception as e:
        logger.exception("Erreur non gérée")
        print(f"Une erreur inattendue s'est produite. Consultez les logs pour plus de détails.")
        sys.exit(1)

if __name__ == '__main__':
    main()

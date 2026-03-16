"""
Validation des fichiers JSON selon les formats Starsector.

Ce module fournit les outils de validation pour les différents formats
de fichiers JSON utilisés dans Starsector.
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from enum import Enum

from .models import (
    ValidationResult,
    ComparisonResult,
    VariableValidation,
    TIPS_FORMAT,
    TOOLTIPS_FORMAT,
    STRINGS_FORMAT,
    SYSTEM_VARIABLES
)
from ..starsector_json import parse_starsector_json, format_starsector_json

class FileType(Enum):
    STRINGS = 1
    TIPS = 2
    TOOLTIPS = 3
    DESCRIPTIONS = 4


class JsonValidator:
    """Validateur de fichiers JSON pour Starsector."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialise le validateur JSON.

        Args:
            logger: Logger pour la journalisation (optionnel, crée un logger par défaut si non fourni)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.format_validators = {
            "tips": self._validate_tips_format,
            "tooltips": self._validate_tooltips_format,
            "strings": self._validate_strings_format
        }
    
    def validate_format(self, content: Union[Dict, List], file_type: FileType) -> ValidationResult:
        """
        Valide le format JSON selon le type de fichier.

        Args:
            content: Contenu JSON à valider
            file_type: Type de fichier (STRINGS, TIPS, TOOLTIPS, DESCRIPTIONS)

        Returns:
            ValidationResult: Résultat de la validation
        """
        try:
            if file_type == FileType.STRINGS:
                if not isinstance(content, dict) or "strings" not in content:
                    return ValidationResult(success=False, format_type="error", 
                        message="Format strings.json invalide : doit contenir une clé 'strings'")
                
                # Validation des variables système
                invalid_vars = set()
                for string_id, string_data in content["strings"].items():
                    if "text" not in string_data:
                        return ValidationResult(success=False, format_type="error",
                            message=f"Format strings.json invalide : 'text' manquant dans {string_id}")
                    
                    # Extraction des variables ($var)
                    text = string_data["text"]
                    vars_in_text = {f"${match.group(1)}" for match in re.finditer(r'\$(\w+)', text)}
                    
                    # Vérification des variables
                    invalid_in_text = vars_in_text - SYSTEM_VARIABLES
                    if invalid_in_text:
                        invalid_vars.update(invalid_in_text)
                
                if invalid_vars:
                    return ValidationResult(success=False, format_type="error",
                        message=f"Variables système invalides trouvées : {', '.join(sorted(invalid_vars))}")
                
                # Validation réussie
                return ValidationResult(success=True, format_type=file_type.name.lower(),
                    message="Format strings.json valide")
            
            elif file_type == FileType.TIPS:
                if not isinstance(content, dict) or "tips" not in content:
                    return ValidationResult(success=False, format_type="error", 
                        message="Format tips.json invalide : doit contenir une clé 'tips'")
            
            elif file_type == FileType.TOOLTIPS:
                if not isinstance(content, dict) or not ("codex" in content or "warroom" in content):
                    return ValidationResult(success=False, format_type="error", 
                        message="Format tooltips.json invalide : doit contenir 'codex' ou 'warroom'")
            
            elif file_type == FileType.DESCRIPTIONS:
                if not isinstance(content, list):
                    return ValidationResult(success=False, format_type="error", 
                        message="Format descriptions.json invalide : doit être une liste")
                
                for item in content:
                    if not all(key in item for key in ["key", "original", "translation", "stage"]):
                        return ValidationResult(success=False, format_type="error", 
                            message="Format descriptions.json invalide : chaque item doit avoir key, original, translation et stage")
        
            return ValidationResult(success=True, format_type=file_type.name.lower(), 
                message=f"Format {file_type.name.lower()} valide")
    
        except Exception as e:
            return ValidationResult(success=False, format_type="error", 
                message=f"Erreur inattendue : {str(e)}")
    
    def validate_variables(self, file_path: Path) -> VariableValidation:
        """
        Valide les variables système dans un fichier.
        
        Args:
            file_path: Chemin du fichier à valider
            
        Returns:
            Résultat de la validation
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Trouve toutes les variables ($xxx)
            variables = set(re.findall(r'\$\w+', content))
            
            # Vérifie les variables inconnues
            invalid_vars = variables - SYSTEM_VARIABLES
            
            return VariableValidation(
                success=(len(invalid_vars) == 0),
                variables=variables,
                invalid_vars=invalid_vars
            )
        except Exception as e:
            self.logger.error(f"Erreur lors de la validation des variables : {e}")
            return VariableValidation(
                success=False,
                variables=set(),
                invalid_vars=set()
            )
    
    def validate_against_original(self, file_path: Path, original: dict) -> ComparisonResult:
        """
        Compare la structure d'un fichier JSON avec l'original.
        
        Args:
            file_path: Chemin du fichier à comparer
            original: Structure originale
            
        Returns:
            Résultat de la comparaison
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data, error = parse_starsector_json(f.read())
                if error:
                    return ComparisonResult(
                        valid_structure=False,
                        identical=False,
                        differences=[f"Erreur de parsing : {error}"]
                    )
                current = data
            
            differences = []
            valid_structure = True
            identical = True
            
            def compare_structure(orig: Any, curr: Any, path: str = "") -> None:
                nonlocal valid_structure, identical
                
                if isinstance(orig, dict):
                    if not isinstance(curr, dict):
                        valid_structure = False
                        differences.append(f"{path}: Type incorrect (attendu: dict)")
                        return
                    
                    # Vérifie les clés manquantes/supplémentaires
                    orig_keys = set(orig.keys())
                    curr_keys = set(curr.keys())
                    
                    missing = orig_keys - curr_keys
                    if missing:
                        valid_structure = False
                        differences.append(f"{path}: Clés manquantes {missing}")
                    
                    extra = curr_keys - orig_keys
                    if extra:
                        identical = False
                        differences.append(f"{path}: Clés supplémentaires {extra}")
                    
                    # Compare récursivement les valeurs
                    for key in orig_keys & curr_keys:
                        new_path = f"{path}.{key}" if path else key
                        compare_structure(orig[key], curr[key], new_path)
                
                elif isinstance(orig, list):
                    if not isinstance(curr, list):
                        valid_structure = False
                        differences.append(f"{path}: Type incorrect (attendu: list)")
                        return
                    
                    if len(orig) != len(curr):
                        identical = False
                        differences.append(
                            f"{path}: Longueur différente ({len(orig)} != {len(curr)})"
                        )
                    
                    # Compare les éléments de la liste
                    for i, (o, c) in enumerate(zip(orig, curr)):
                        compare_structure(o, c, f"{path}[{i}]")
                
                elif type(orig) != type(curr):
                    valid_structure = False
                    differences.append(
                        f"{path}: Type incorrect (attendu: {type(orig).__name__})"
                    )
            
            compare_structure(original, current)
            
            return ComparisonResult(
                valid_structure=valid_structure,
                identical=identical,
                differences=differences
            )
            
        except Exception as e:
            return ComparisonResult(
                valid_structure=False,
                identical=False,
                differences=[f"Erreur de comparaison : {str(e)}"]
            )
    
    def _detect_format_type(self, content: dict) -> Optional[str]:
        """
        Détecte le type de format JSON.
        
        Args:
            content: Contenu JSON à analyser
            
        Returns:
            Type de format ou None si non reconnu
        """
        if not isinstance(content, dict):
            return None
        
        # Détection basée sur les champs requis
        if all(field in content for field in TIPS_FORMAT.required_fields):
            return "tips"
        elif all(field in content for field in TOOLTIPS_FORMAT.required_fields):
            return "tooltips"
        elif all(field in content for field in STRINGS_FORMAT.required_fields):
            return "strings"
        
        return None
    
    def _validate_tips_format(self, content: dict) -> ValidationResult:
        """
        Valide le format tips.json.
        
        Args:
            content: Contenu à valider
            
        Returns:
            Résultat de la validation
        """
        if not isinstance(content, dict):
            return ValidationResult(
                success=False,
                format_type="tips",
                message="Le contenu doit être un dictionnaire"
            )
        
        # Vérifie les champs requis
        missing_fields = TIPS_FORMAT.required_fields - set(content.keys())
        if missing_fields:
            return ValidationResult(
                success=False,
                format_type="tips",
                message=f"Champs requis manquants : {missing_fields}"
            )
        
        return ValidationResult(
            success=True,
            format_type="tips"
        )
    
    def _validate_tooltips_format(self, content: dict) -> ValidationResult:
        """
        Valide le format tooltips.json.
        
        Args:
            content: Contenu à valider
            
        Returns:
            Résultat de la validation
        """
        if not isinstance(content, dict):
            return ValidationResult(
                success=False,
                format_type="tooltips",
                message="Le contenu doit être un dictionnaire"
            )
        
        # Vérifie les champs requis
        missing_fields = TOOLTIPS_FORMAT.required_fields - set(content.keys())
        if missing_fields:
            return ValidationResult(
                success=False,
                format_type="tooltips",
                message=f"Champs requis manquants : {missing_fields}"
            )
        
        return ValidationResult(
            success=True,
            format_type="tooltips"
        )
    
    def _validate_strings_format(self, content: dict) -> ValidationResult:
        """
        Valide le format strings.json.
        
        Args:
            content: Contenu à valider
            
        Returns:
            Résultat de la validation
        """
        if not isinstance(content, dict):
            return ValidationResult(
                success=False,
                format_type="strings",
                message="Le contenu doit être un dictionnaire"
            )
        
        # Vérifie les champs requis
        missing_fields = STRINGS_FORMAT.required_fields - set(content.keys())
        if missing_fields:
            return ValidationResult(
                success=False,
                format_type="strings",
                message=f"Champs requis manquants : {missing_fields}"
            )
        
        return ValidationResult(
            success=True,
            format_type="strings"
        )

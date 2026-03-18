#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface principale pour la gestion des fichiers JSON Starsector.
Coordonne les différents modules spécialisés.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Set

from .models import ValidationResult, ComparisonResult, VariableValidation
from .formatter import JsonFormatter
from .validator import JsonValidator

class JsonHandler:
    """Interface principale pour la gestion des fichiers JSON Starsector."""
    
    def __init__(self, logger: logging.Logger):
        """
        Initialise le gestionnaire JSON.
        
        Args:
            logger: Logger pour la journalisation
        """
        self.logger = logger
        self.formatter = JsonFormatter(logger)
        self.validator = JsonValidator(logger)
        
        # Variables système connues
        self.known_variables = {
            "$faction", "$fleetOrShip", "$playerName",
            "$shipName", "$systemName", "$planetName"
        }
    
    def load(self, file_path: Path) -> Optional[Dict]:
        """
        Charge un fichier JSON.
        
        Args:
            file_path: Chemin du fichier à charger
            
        Returns:
            Dict: Contenu du fichier ou None si erreur
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur de lecture JSON : {str(e)}")
            return None
    
    def dump(self, content: Dict, file_path: Path, starsector_format: bool = True) -> bool:
        """
        Écrit un contenu JSON dans un fichier.
        
        Args:
            content: Contenu à écrire
            file_path: Chemin du fichier
            starsector_format: Si True, utilise le format spécifique de Starsector
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            json_str = self.formatter.format_json_string(content, starsector_format)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            return True
        except Exception as e:
            self.logger.error(f"Erreur d'écriture JSON : {str(e)}")
            return False
    
    def validate_format(self, file_path: Path) -> ValidationResult:
        """
        Valide le format d'un fichier JSON.
        
        Args:
            file_path: Chemin du fichier à valider
            
        Returns:
            ValidationResult: Résultat de la validation
        """
        content = self.load(file_path)
        if content is None:
            return ValidationResult(False, "", "Erreur de lecture du fichier")
        return self.validator.validate_format(content)
    
    def validate_variables(self, file_path: Path) -> VariableValidation:
        """
        Valide les variables système dans un fichier.
        
        Args:
            file_path: Chemin du fichier à valider
            
        Returns:
            VariableValidation: Résultat de la validation
        """
        content = self.load(file_path)
        if content is None:
            return VariableValidation(False, set(), set())
        return self.validator.validate_variables(content, self.known_variables)
    
    def validate_against_original(self, file_path: Path, original: Dict) -> ComparisonResult:
        """
        Compare la structure d'un fichier JSON avec l'original.
        
        Args:
            file_path: Chemin du fichier à comparer
            original: Structure originale
            
        Returns:
            ComparisonResult: Résultat de la comparaison
        """
        content = self.load(file_path)
        if content is None:
            return ComparisonResult(False, False, ["Erreur de lecture du fichier"])
        return self.validator.validate_against_original(content, original)
    
    def fix_quotes(self, file_path: Path) -> bool:
        """
        Convertit les guillemets droits en guillemets français dans un fichier JSON.
        
        Args:
            file_path: Chemin du fichier à traiter
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            content = self.load(file_path)
            if content is None:
                return False
            
            # Convertit les guillemets dans toutes les chaînes
            formatted = self.formatter.process_json_data(content)
            
            # Sauvegarde le résultat
            return self.dump(formatted, file_path)
            
        except Exception as e:
            self.logger.error(f"Erreur de conversion des guillemets : {str(e)}")
            return False

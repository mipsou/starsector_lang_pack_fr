#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gestionnaire des fichiers de mission pour Starsector.
Valide la structure et le contenu des fichiers de mission.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from utils.format_utils import FormatUtils

@dataclass
class ValidationResult:
    """Résultat de validation d'un fichier."""
    success: bool
    message: str
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class MissionHandler:
    """Gestionnaire des fichiers de mission."""
    
    def __init__(self):
        """Initialisation du gestionnaire."""
        self.format_utils = FormatUtils()
        self.required_fields = ['Lieu', 'Date', 'Objectifs', 'Description']
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Valide un fichier de mission."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Normalisation du contenu
            content = self.format_utils.normalize_newlines(content)
            content = self.format_utils.fix_quotes(content)
            
            # Extraction des champs
            fields = {}
            current_field = None
            current_content = []
            
            for line in content.split('\n'):
                if ':' in line:
                    if current_field:
                        fields[current_field] = '\n'.join(current_content).strip()
                        current_content = []
                    
                    field, value = line.split(':', 1)
                    current_field = field.strip()
                    current_content.append(value.strip())
                elif line.strip() and current_field:
                    current_content.append(line.strip())
            
            if current_field:
                fields[current_field] = '\n'.join(current_content).strip()
            
            # Validation des champs requis
            missing_fields = [field for field in self.required_fields if field not in fields]
            if missing_fields:
                return ValidationResult(
                    success=False,
                    message='Structure invalide',
                    errors=[f'Champ requis manquant : {field}' for field in missing_fields]
                )
            
            # Validation du contenu des champs
            errors = []
            for field, content in fields.items():
                if not content:
                    errors.append(f'Le champ {field} est vide')
            
            if errors:
                return ValidationResult(
                    success=False,
                    message='Contenu invalide',
                    errors=errors
                )
            
            return ValidationResult(
                success=True,
                message='Fichier de mission valide'
            )
            
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f'Erreur lors de la validation : {str(e)}'
            )

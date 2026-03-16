"""
Module d'écriture JSON pour Starsector.

Ce module fournit les fonctionnalités d'écriture sécurisée des fichiers JSON
avec validation automatique et backup intégré.

Cas d'utilisation :
1. Écriture de fichiers JSON
   >>> writer = JsonWriter()
   >>> content = {"strings": {"id": {"text": "Test"}}}
   >>> result = writer.write_json(content, Path("strings.json"))

2. Mise à jour partielle
   >>> updates = {"strings": {"new_id": {"text": "New"}}}
   >>> result = writer.update_json(Path("strings.json"), updates)

3. Gestion des fichiers spéciaux
   - tips.json : Liste de conseils
   - descriptions.json : Descriptions d'items
   - tooltips.json : Infobulles
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .validator import JsonValidator, FileType
from .models import ValidationResult
from ..starsector_json import format_starsector_json, parse_starsector_json, detect_file_type
from .handler import JsonHandler

# Initialisation du handler JSON
logger = logging.getLogger(__name__)
json_handler = JsonHandler(logger)


class JsonWriter:
    """Écrivain de fichiers JSON pour Starsector."""
    
    def __init__(self, validator: Optional[JsonValidator] = None):
        """
        Initialise l'écrivain JSON.
        
        Args:
            validator: Validateur JSON optionnel. Si non fourni, crée une nouvelle instance.
        """
        self.validator = validator if validator is not None else JsonValidator()
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self, file_path: Path) -> Path:
        """
        Crée une sauvegarde du fichier.

        Args:
            file_path: Chemin du fichier à sauvegarder

        Returns:
            Path: Chemin de la sauvegarde
        """
        if not file_path.exists():
            return file_path

        # Création du dossier backup si nécessaire
        backup_dir = file_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Nom du fichier de backup avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"

        # Copie du fichier
        shutil.copy2(file_path, backup_path)

        return backup_path
    
    def write_json(self, content: Dict[str, Any], file_path: Path, file_type: Optional[FileType] = None) -> ValidationResult:
        """
        Écrit le contenu JSON dans un fichier.

        Args:
            content: Contenu à écrire
            file_path: Chemin du fichier
            file_type: Type de fichier (optionnel, détecté automatiquement si non fourni)

        Returns:
            ValidationResult: Résultat de la validation
        """
        try:
            self.logger.info(f"Début écriture fichier : {file_path}")
            
            # Détection ou utilisation du type de fichier fourni
            detected_type = file_type if file_type else detect_file_type(content)
            if not detected_type:
                self.logger.error(f"Type de fichier non reconnu : {file_path}")
                return ValidationResult(
                    success=False, 
                    format_type="error", 
                    message="Type de fichier non reconnu",
                    backup_path=None
                )

            # Validation du contenu
            self.logger.debug("Validation du contenu...")
            validation = self.validator.validate_format(content, detected_type)
            if not validation.success:
                self.logger.error(f"Échec validation : {validation.message}")
                return validation
            
            # Création du backup
            backup_path = self.create_backup(file_path)
            self.logger.info(f"Backup créé : {backup_path}")

            # Formatage et écriture du fichier
            formatted_json = format_starsector_json(content, detected_type)
            if not formatted_json:
                self.logger.error("Échec du formatage JSON")
                return ValidationResult(
                    success=False,
                    format_type="error",
                    message="Échec du formatage JSON",
                    backup_path=backup_path
                )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(formatted_json)
            
            self.logger.info(f"Fichier écrit avec succès : {file_path}")
            return ValidationResult(
                success=True, 
                format_type=detected_type.name.lower(),
                message=f"Fichier {file_path.name} écrit avec succès",
                backup_path=backup_path
            )
        
        except Exception as e:
            self.logger.error(f"Erreur lors de l'écriture : {str(e)}")
            return ValidationResult(
                success=False, 
                format_type="error",
                message=f"Erreur inattendue : {str(e)}",
                backup_path=None
            )

    def update_json(self, file_path: Path, updates: Dict[str, Any]) -> ValidationResult:
        """
        Met à jour un fichier JSON existant.

        Args:
            file_path: Chemin du fichier à mettre à jour
            updates: Mises à jour à appliquer

        Returns:
            ValidationResult: Résultat de la mise à jour
        """
        try:
            # Lecture du fichier existant
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                current_content, error = parse_starsector_json(content)
                if error:
                    return ValidationResult(success=False, format_type="error", 
                        message=f"Erreur de lecture : {error}")
            
            # Mise à jour du contenu
            for key, value in updates.items():
                if key in current_content:
                    if isinstance(current_content[key], dict):
                        current_content[key].update(value)
                    else:
                        current_content[key] = value
                else:
                    current_content[key] = value
            
            # Écriture du fichier mis à jour
            return self.write_json(current_content, file_path)

        except Exception as e:
            return ValidationResult(success=False, format_type="error", 
                message=f"Erreur de mise à jour : {str(e)}")

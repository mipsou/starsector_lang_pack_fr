#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilitaires de gestion des chemins pour le système de traduction Starsector.
Gère les chemins, les sauvegardes et la validation des accès aux fichiers.
"""

import os
import shutil
import time
from pathlib import Path
from typing import List, Optional, Tuple
from .logging_utils import setup_logger

logger = setup_logger(__name__)

class PathManager:
    """Gestionnaire de chemins pour le système de traduction."""
    
    def __init__(self, base_dir: str):
        """
        Initialise le gestionnaire de chemins.
        
        Args:
            base_dir: Répertoire de base du mod
        """
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "backup"
        self.temp_dir = self.base_dir / "temp"
        self.config_dir = self.base_dir / "config"
        
        # Préfère les fichiers .local.conf
        self.config_local = self.config_dir / "translation.local.conf"
        self.config_default = self.config_dir / "translation.conf"
        
        # Crée les répertoires nécessaires
        self._create_directories()
    
    def _create_directories(self):
        """Crée les répertoires nécessaires s'ils n'existent pas."""
        for directory in [self.backup_dir, self.temp_dir, self.config_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_config_path(self) -> Path:
        """
        Retourne le chemin du fichier de configuration à utiliser.
        Préfère le fichier .local.conf s'il existe.
        """
        if self.config_local.exists():
            return self.config_local
        return self.config_default
    
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Crée une sauvegarde d'un fichier.
        
        Args:
            file_path: Chemin du fichier à sauvegarder
            
        Returns:
            Chemin de la sauvegarde ou None si erreur
        """
        try:
            if not file_path.exists():
                logger.warning(f"Fichier non trouvé pour backup : {file_path}")
                return None
            
            # Crée un nom unique avec timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            # Copie le fichier
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backup créé : {backup_path}")
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du backup : {str(e)}")
            return None
    
    def backup_file(self, file_path: str, backup_dir: Optional[str] = None) -> Optional[Path]:
        """
        Crée une sauvegarde d'un fichier.
        
        Args:
            file_path: Chemin du fichier à sauvegarder
            backup_dir: Répertoire de sauvegarde optionnel
            
        Returns:
            Chemin de la sauvegarde ou None si erreur
        """
        file_path = Path(file_path)
        backup_dir = Path(backup_dir) if backup_dir else self.backup_dir
        
        return self.create_backup(file_path)
    
    def get_preferred_config_path(self, config_path: str) -> Path:
        """
        Retourne le chemin du fichier de configuration préféré.
        Préfère le fichier .local.conf s'il existe.
        
        Args:
            config_path: Chemin du fichier de configuration
            
        Returns:
            Chemin du fichier de configuration à utiliser
        """
        config_path = Path(config_path)
        local_path = config_path.parent / f"{config_path.stem}.local{config_path.suffix}"
        
        if local_path.exists():
            return local_path
        return config_path
    
    def validate_path(self, path: Path) -> Tuple[bool, str]:
        """
        Valide un chemin de fichier.
        
        Args:
            path: Chemin à valider
            
        Returns:
            Tuple (valide: bool, message: str)
        """
        try:
            # Vérifie que le chemin est absolu
            if not path.is_absolute():
                return False, "Le chemin doit être absolu"
            
            # Vérifie que le chemin est dans le répertoire du mod ou dans un répertoire temporaire
            try:
                path.relative_to(self.base_dir)
            except ValueError:
                # Si le chemin n'est pas dans le répertoire du mod, vérifie s'il est dans un répertoire temporaire
                if not any(temp in str(path).lower() for temp in ['temp', 'tmp']):
                    return False, "Le chemin doit être dans le répertoire du mod ou un répertoire temporaire"
            
            # Vérifie les permissions si le fichier existe
            if path.exists():
                try:
                    if path.is_file():
                        with open(path, 'a') as _:
                            pass
                    else:
                        # Test d'écriture dans le répertoire
                        test_file = path / '.write_test'
                        test_file.touch()
                        test_file.unlink()
                except IOError:
                    return False, "Permissions insuffisantes"
            
            return True, "Chemin valide"
            
        except Exception as e:
            return False, f"Erreur de validation : {str(e)}"
    
    def list_files(self, directory: str, pattern: str = "*") -> List[Path]:
        """
        Liste les fichiers dans un répertoire selon un pattern.
        
        Args:
            directory: Répertoire à scanner
            pattern: Pattern de fichier (ex: "*.json")
            
        Returns:
            Liste des chemins de fichiers
        """
        try:
            directory = Path(directory)
            if not directory.is_dir():
                logger.error(f"Répertoire invalide : {directory}")
                return []
            
            return list(directory.glob(pattern))
            
        except Exception as e:
            logger.error(f"Erreur lors du listage des fichiers : {str(e)}")
            return []
    
    def ensure_dir(self, path: Path) -> bool:
        """
        S'assure qu'un répertoire existe, le crée si nécessaire.
        
        Args:
            path: Chemin du répertoire
            
        Returns:
            True si le répertoire existe ou a été créé
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la création du répertoire : {str(e)}")
            return False
    
    def ensure_directory(self, path: str) -> bool:
        """
        S'assure qu'un répertoire existe, le crée si nécessaire.
        
        Args:
            path: Chemin du répertoire
            
        Returns:
            True si le répertoire existe ou a été créé
        """
        return self.ensure_dir(Path(path))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration et utilitaires de logging pour le système de traduction Starsector.
Gère la configuration des logs, leur rotation et les différents niveaux de verbosité.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

class LogConfig:
    """Configuration du système de logging."""
    
    def __init__(self, log_dir: str = "logs", name: str = "translation"):
        """
        Initialise la configuration des logs.
        
        Args:
            log_dir: Répertoire des fichiers de log
            name: Nom de base du fichier de log
        """
        self.log_dir = Path(log_dir)
        self.log_file = self.log_dir / f"{name}.log"
        self.max_bytes = 1024  # 1 KB pour les tests, 5 MB en production
        self.backup_count = 5
        self.format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        
        # Crée le répertoire des logs s'il n'existe pas
        self.log_dir.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str, 
                level: int = logging.INFO,
                config: Optional[LogConfig] = None) -> logging.Logger:
    """
    Configure et retourne un logger.
    
    Args:
        name: Nom du logger
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        config: Configuration personnalisée
        
    Returns:
        Logger configuré
    """
    if config is None:
        config = LogConfig(name=name)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Évite les handlers en double
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler pour fichier avec rotation
    file_handler = logging.handlers.RotatingFileHandler(
        config.log_file,
        maxBytes=config.max_bytes,
        backupCount=config.backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter(config.format, config.date_format)
    )
    logger.addHandler(file_handler)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(config.format, config.date_format)
    )
    logger.addHandler(console_handler)
    
    return logger

def log_exception(logger: logging.Logger, 
                 e: Exception, 
                 message: str = "Une erreur est survenue"):
    """
    Log une exception avec son contexte.
    
    Args:
        logger: Logger à utiliser
        e: Exception à logger
        message: Message descriptif
    """
    logger.error(f"{message}: {str(e)}", exc_info=True)

# Logger par défaut
default_logger = setup_logger("starsector_translation")

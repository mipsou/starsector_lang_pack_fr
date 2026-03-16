"""
Convertisseur JSON avec support de la typographie française.

Ce module réutilise les fonctionnalités de StringHandler pour
la gestion des guillemets et de la typographie française.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

from ..string_handler import StringHandler


class JsonConverter:
    """Convertisseur de fichiers JSON avec support typographique."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialise le convertisseur JSON.
        
        Args:
            logger: Logger pour la journalisation
        """
        self.logger = logger or logging.getLogger(__name__)
        self.string_handler = StringHandler()
    
    def convert_file(self, file_path: Path) -> bool:
        """
        Convertit un fichier JSON en appliquant les règles typographiques.
        
        Args:
            file_path: Chemin du fichier à convertir
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Lecture du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # Conversion des chaînes
            converted = self._convert_data(content)
            
            # Écriture du résultat
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(converted, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la conversion de {file_path}: {e}")
            return False
    
    def _convert_data(self, data: Any) -> Any:
        """
        Convertit récursivement les données JSON.
        
        Args:
            data: Données à convertir
            
        Returns:
            Données converties
        """
        if isinstance(data, dict):
            return {k: self._convert_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_data(item) for item in data]
        elif isinstance(data, str):
            return self.string_handler.convert_json_string(data)
        else:
            return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de formatage JSON pour Starsector.
Gère la conversion des guillemets et le formatage spécifique.
"""

import re
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

class JsonFormatter:
    """Formateur de fichiers JSON pour Starsector."""
    
    def __init__(self, logger: logging.Logger):
        """
        Initialise le formateur JSON.
        
        Args:
            logger: Logger pour la journalisation
        """
        self.logger = logger
    
    def convert_quotes(self, text: Union[str, Path]) -> str:
        """
        Convertit les guillemets droits en guillemets français avec gestion des guillemets imbriqués.
        
        Args:
            text: Texte ou chemin du fichier à traiter
            
        Returns:
            str: Texte avec guillemets convertis
        """
        if isinstance(text, Path):
            try:
                with open(text, 'r', encoding='utf-8') as f:
                    content = f.read()
                return self.convert_quotes(content)
            except Exception as e:
                self.logger.error(f"Erreur lors de la lecture du fichier {text}: {str(e)}")
                return str(text)

        if not text:
            return text

        # Si le texte contient des guillemets non appariés, le retourner tel quel
        if text.count('"') % 2 != 0:
            return text

        # Préserver les guillemets JSON externes
        is_json_string = text.startswith('"') and text.endswith('"')
        first_quote = '"' if is_json_string else ''
        last_quote = '"' if is_json_string else ''
        content = text[1:-1] if is_json_string else text

        # Compter les guillemets pour déterminer le niveau d'imbrication
        quote_positions = []
        i = 0
        while i < len(content):
            if i < len(content) - 1 and content[i:i+2] == '\\"':
                quote_positions.append(i)
                i += 2
            elif content[i] == '"' and (i == 0 or content[i-1] != '\\'):
                quote_positions.append(i)
                i += 1
            else:
                i += 1

        # Traiter les guillemets par paires
        result = list(content)
        for i in range(0, len(quote_positions), 2):
            if i + 1 < len(quote_positions):
                start = quote_positions[i]
                end = quote_positions[i + 1]
                
                # Remplacer les guillemets
                if result[start:start+2] == ['\\', '"']:
                    result[start:start+2] = ['«']
                else:
                    result[start] = '«'
                
                if end > 0 and result[end-1:end+1] == ['\\', '"']:
                    result[end-1:end+1] = ['»']
                else:
                    result[end] = '»'
                
                # Ajouter des espaces si nécessaire
                if start + 1 < len(result) and result[start + 1] not in [' ', '»']:
                    result.insert(start + 1, ' ')
                    # Mettre à jour les positions suivantes
                    for j in range(i + 1, len(quote_positions)):
                        quote_positions[j] += 1
                
                if end - 1 >= 0 and result[end - 1] not in [' ', '«']:
                    result.insert(end, ' ')
                    # Mettre à jour les positions suivantes
                    for j in range(i + 2, len(quote_positions)):
                        quote_positions[j] += 1

        # Nettoyer les espaces multiples et les espaces avant la ponctuation
        text = ''.join(result)
        text = ' '.join(text.split())
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        
        # Nettoyer les espaces entre guillemets imbriqués
        text = re.sub(r'»\s+«', r'» «', text)
        text = re.sub(r'«\s+«', r'«', text)
        text = re.sub(r'»\s+»', r'»', text)

        return first_quote + text + last_quote
    
    def process_json_data(self, data: Any) -> Any:
        """
        Traite les données JSON pour convertir les guillemets.
        
        Args:
            data: Les données JSON à traiter
            
        Returns:
            Any: Les données JSON avec les guillemets convertis
        """
        if isinstance(data, dict):
            return {k: self.process_json_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_json_data(item) for item in data]
        elif isinstance(data, str):
            return self.convert_quotes(data)
        else:
            return data
    
    def format_json_string(self, content: dict, starsector_format: bool = True) -> str:
        """
        Formate une chaîne JSON selon les conventions Starsector.
        
        Args:
            content: Contenu à formater
            starsector_format: Si True, utilise le format spécifique de Starsector
            
        Returns:
            str: Chaîne JSON formatée
        """
        try:
            if starsector_format:
                # Convertit en JSON avec indentation
                json_str = json.dumps(content, ensure_ascii=False, indent=4)
                # Ajoute les virgules finales requises par le format Starsector
                json_str = re.sub(r'([}\]])(,?\s*[}\]])', r'\1,\2', json_str)
                return json_str
            else:
                return json.dumps(content, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.error(f"Erreur de formatage JSON : {str(e)}")
            return ""

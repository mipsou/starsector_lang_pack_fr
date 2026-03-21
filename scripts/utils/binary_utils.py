"""
Utilitaires pour l'analyse binaire des fichiers.

Ce module fournit des fonctions pour l'analyse et le diagnostic des fichiers
au niveau binaire, notamment pour la détection des caractères de contrôle.
"""

import os
from pathlib import Path


def find_control_chars_binary(file_path):
    """
    Trouve les caractères de contrôle dans un fichier en mode binaire.
    
    Cette fonction analyse un fichier octet par octet pour détecter les caractères
    de contrôle qui pourraient causer des problèmes dans les fichiers JSON de
    Starsector.
    
    Args:
        file_path (str): Chemin du fichier à analyser
        
    Returns:
        list: Liste des caractères de contrôle trouvés avec leur position
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        Exception: Pour toute autre erreur lors de l'analyse
    """
    file_path = Path(file_path)
    control_chars = []
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        for i, byte in enumerate(content):
            # Vérifie si c'est un caractère de contrôle
            if byte < 32 and byte not in (9, 10, 13):  # Tab, LF, CR sont ok
                control_chars.append((i, hex(byte)))
        
        return control_chars
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse : {str(e)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Outil d'extraction sécurisée des fichiers JAR pour Starsector
Compatible Java 7 (1.7.0_79-b15)

Cet outil :
1. Extrait les fichiers des JAR de manière sécurisée
2. Maintient des backups
3. Valide l'intégrité des fichiers
"""

import os
import sys
import shutil
import hashlib
import zipfile
import logging
from datetime import datetime
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jar_extractor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class JarExtractor:
    def __init__(self, jar_path, output_dir):
        """
        Initialise l'extracteur de JAR.
        
        :param jar_path: Chemin vers le fichier JAR
        :param output_dir: Dossier de sortie pour les fichiers extraits
        """
        self.jar_path = Path(jar_path)
        self.output_dir = Path(output_dir)
        self.backup_dir = self.output_dir / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_backup(self):
        """Crée une sauvegarde du JAR original."""
        try:
            self.backup_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.jar_path, self.backup_dir / self.jar_path.name)
            logging.info(f"Backup créé : {self.backup_dir / self.jar_path.name}")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la création du backup : {e}")
            return False

    def calculate_hash(self, file_path):
        """Calcule le hash SHA-256 d'un fichier."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def extract_files(self, file_patterns=None):
        """
        Extrait les fichiers du JAR.
        
        :param file_patterns: Liste de patterns de fichiers à extraire
        :return: True si succès, False sinon
        """
        try:
            if not self.create_backup():
                return False

            with zipfile.ZipFile(self.jar_path, 'r') as jar:
                for item in jar.namelist():
                    if file_patterns and not any(pattern in item for pattern in file_patterns):
                        continue
                    
                    # Créer le dossier de destination
                    output_path = self.output_dir / item
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extraire le fichier
                    with jar.open(item) as source, open(output_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                    
                    # Vérifier l'intégrité
                    with jar.open(item) as source:
                        original_content = source.read()
                        with open(output_path, 'rb') as target:
                            extracted_content = target.read()
                            if original_content != extracted_content:
                                logging.error(f"Erreur d'intégrité pour {item}")
                                return False
                    
                    logging.info(f"Fichier extrait et vérifié : {item}")
            
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction : {e}")
            return False

def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 3:
        print("Usage: jar_extractor.py <jar_path> <output_dir> [pattern1 pattern2 ...]")
        sys.exit(1)
    
    jar_path = sys.argv[1]
    output_dir = sys.argv[2]
    patterns = sys.argv[3:] if len(sys.argv) > 3 else None
    
    extractor = JarExtractor(jar_path, output_dir)
    if extractor.extract_files(patterns):
        logging.info("Extraction terminée avec succès")
    else:
        logging.error("Échec de l'extraction")
        sys.exit(1)

if __name__ == "__main__":
    main()

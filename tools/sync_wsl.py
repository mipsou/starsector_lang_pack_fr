#!/usr/bin/env python3
"""
Script de synchronisation entre Windows et WSL2.
Permet de synchroniser les fichiers de traduction et les résultats de traitement.
"""

import os
import sys
import json
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync_wsl.log'),
        logging.StreamHandler()
    ]
)

class WSLSyncManager:
    def __init__(self, windows_path: str, wsl_path: str):
        """Initialise le gestionnaire de synchronisation."""
        self.windows_path = Path(windows_path)
        self.wsl_path = wsl_path
        
    def to_wsl_path(self, windows_path: Path) -> str:
        """Convertit un chemin Windows en chemin WSL."""
        # Exemple: D:\projet -> /mnt/d/projet
        parts = windows_path.absolute().parts
        drive = parts[0].lower().replace(':', '')
        rest = '/'.join(parts[1:])
        return f"/mnt/{drive}/{rest}"
    
    def to_windows_path(self, wsl_path: str) -> Path:
        """Convertit un chemin WSL en chemin Windows."""
        # Exemple: /mnt/d/projet -> D:\projet
        parts = wsl_path.split('/')
        if len(parts) > 2 and parts[1] == 'mnt':
            drive = f"{parts[2].upper()}:"
            rest = '\\'.join(parts[3:])
            return Path(f"{drive}\\{rest}")
        return None
    
    def sync_to_wsl(self) -> bool:
        """Synchronise les fichiers vers WSL."""
        try:
            wsl_project_path = self.to_wsl_path(self.windows_path)
            
            # Création du répertoire dans WSL
            cmd = [
                'wsl',
                'mkdir',
                '-p',
                wsl_project_path
            ]
            subprocess.run(cmd, check=True)
            
            # Synchronisation des fichiers
            cmd = [
                'wsl',
                'rsync',
                '-av',
                '--delete',
                self.to_wsl_path(self.windows_path) + '/',
                self.wsl_path + '/'
            ]
            subprocess.run(cmd, check=True)
            
            logging.info(f"Synchronisation vers WSL réussie")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de la synchronisation vers WSL : {str(e)}")
            return False
    
    def sync_from_wsl(self) -> bool:
        """Synchronise les fichiers depuis WSL."""
        try:
            # Synchronisation des résultats
            cmd = [
                'wsl',
                'rsync',
                '-av',
                '--delete',
                f"{self.wsl_path}/results/",
                self.to_wsl_path(self.windows_path / 'results') + '/'
            ]
            subprocess.run(cmd, check=True)
            
            logging.info(f"Synchronisation depuis WSL réussie")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de la synchronisation depuis WSL : {str(e)}")
            return False
    
    def run_wsl_command(self, command: str) -> Tuple[bool, str]:
        """Exécute une commande dans WSL."""
        try:
            result = subprocess.run(
                ['wsl', 'bash', '-c', command],
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de l'exécution de la commande WSL : {str(e)}")
            return False, str(e)

def main():
    """Point d'entrée principal."""
    import argparse
    parser = argparse.ArgumentParser(
        description='Synchronise les fichiers entre Windows et WSL.'
    )
    parser.add_argument(
        'windows_path',
        help='Chemin du projet Windows'
    )
    parser.add_argument(
        'wsl_path',
        help='Chemin du projet dans WSL'
    )
    parser.add_argument(
        '--direction',
        choices=['to-wsl', 'from-wsl'],
        required=True,
        help='Direction de la synchronisation'
    )
    args = parser.parse_args()
    
    sync_manager = WSLSyncManager(args.windows_path, args.wsl_path)
    
    if args.direction == 'to-wsl':
        success = sync_manager.sync_to_wsl()
    else:
        success = sync_manager.sync_from_wsl()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())

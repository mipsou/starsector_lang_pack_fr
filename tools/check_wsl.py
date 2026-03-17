#!/usr/bin/env python3
"""
Script de vérification de l'environnement WSL.
"""

import subprocess
import logging
import json
from typing import Dict, List, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('check_wsl.log'),
        logging.StreamHandler()
    ]
)

def check_wsl_version() -> Tuple[bool, str]:
    """Vérifie la version de WSL."""
    try:
        result = subprocess.run(
            ['wsl', '--version'],
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, str(e)

def check_systemd() -> Tuple[bool, str]:
    """Vérifie si systemd est actif."""
    try:
        result = subprocess.run(
            ['wsl', 'systemctl', 'status'],
            capture_output=True,
            text=True
        )
        return 'running' in result.stdout.lower(), result.stdout
    except subprocess.CalledProcessError as e:
        return False, str(e)

def check_gpu() -> Tuple[bool, str]:
    """Vérifie la disponibilité du GPU."""
    try:
        result = subprocess.run(
            ['wsl', 'rocm-smi'],
            capture_output=True,
            text=True
        )
        return 'GPU' in result.stdout, result.stdout
    except subprocess.CalledProcessError as e:
        return False, str(e)

def check_python_packages() -> Dict[str, bool]:
    """Vérifie les packages Python installés."""
    packages = {
        'torch': False,
        'torchvision': False,
        'numpy': False,
        'pillow': False
    }
    
    try:
        for package in packages:
            result = subprocess.run(
                ['wsl', 'python3', '-c', f'import {package}'],
                capture_output=True,
                text=True
            )
            packages[package] = result.returncode == 0
    except subprocess.CalledProcessError:
        pass
    
    return packages

def main():
    """Point d'entrée principal."""
    results = {
        'wsl': {},
        'systemd': {},
        'gpu': {},
        'python_packages': {}
    }
    
    # Vérification WSL
    success, output = check_wsl_version()
    results['wsl'] = {
        'status': success,
        'version': output if success else 'Non disponible'
    }
    
    # Vérification systemd
    success, output = check_systemd()
    results['systemd'] = {
        'status': success,
        'output': output if success else 'Non disponible'
    }
    
    # Vérification GPU
    success, output = check_gpu()
    results['gpu'] = {
        'status': success,
        'output': output if success else 'Non disponible'
    }
    
    # Vérification packages Python
    results['python_packages'] = check_python_packages()
    
    # Affichage des résultats
    print("\nRésultats de la vérification WSL :")
    print("-" * 50)
    
    # WSL
    print("\n1. WSL")
    print(f"Status : {'✓' if results['wsl']['status'] else '✗'}")
    print(f"Version : {results['wsl']['version']}")
    
    # systemd
    print("\n2. systemd")
    print(f"Status : {'✓' if results['systemd']['status'] else '✗'}")
    if results['systemd']['status']:
        print("systemd est actif")
    
    # GPU
    print("\n3. GPU")
    print(f"Status : {'✓' if results['gpu']['status'] else '✗'}")
    if results['gpu']['status']:
        print(results['gpu']['output'])
    
    # Packages Python
    print("\n4. Packages Python")
    for package, installed in results['python_packages'].items():
        print(f"{package}: {'✓' if installed else '✗'}")
    
    # Sauvegarde des résultats
    with open('wsl_check_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Retourne 0 si tout est OK, 1 sinon
    return 0 if all([
        results['wsl']['status'],
        results['systemd']['status'],
        results['gpu']['status'],
        all(results['python_packages'].values())
    ]) else 1

if __name__ == "__main__":
    exit(main())

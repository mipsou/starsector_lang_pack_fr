#!/usr/bin/env python
"""
Script de vérification et configuration de l'environnement.
Vérifie et configure l'encodage, les chemins et les dépendances.
"""
import os
import sys
import locale
import subprocess
from pathlib import Path

def check_terminal_encoding():
    """Vérifie l'encodage du terminal."""
    print(f"Encodage stdin  : {sys.stdin.encoding}")
    print(f"Encodage stdout : {sys.stdout.encoding}")
    print(f"Encodage stderr : {sys.stderr.encoding}")
    print(f"Encodage par défaut : {sys.getdefaultencoding()}")
    print(f"Locale système : {locale.getpreferredencoding()}")

def set_utf8_encoding():
    """Configure l'encodage UTF-8 pour le terminal."""
    if os.name == 'nt':  # Windows
        try:
            subprocess.run(['chcp', '65001'], check=True)
            os.system('') # Réinitialise le terminal
            return True
        except subprocess.CalledProcessError:
            print("Erreur : Impossible de configurer l'UTF-8")
            return False
    return True

def check_python_path():
    """Vérifie la configuration du PATH Python."""
    scripts_path = Path(sys.executable).parent / 'Scripts'
    if os.name == 'nt':  # Windows
        path = os.environ.get('PATH', '').split(os.pathsep)
        if str(scripts_path) not in path:
            print(f"ATTENTION : {scripts_path} n'est pas dans le PATH")
            print("Ajoutez-le au PATH ou utilisez le chemin complet")
        else:
            print(f"Python Scripts dans le PATH : {scripts_path}")

def main():
    """Fonction principale."""
    print("\n=== Vérification de l'Environnement ===\n")
    
    # Configuration UTF-8
    print("Configuration UTF-8...")
    if set_utf8_encoding():
        print("✓ Encodage UTF-8 configuré")
    else:
        print("✗ Erreur de configuration UTF-8")
    
    # Vérification de l'encodage
    print("\nVérification des encodages...")
    check_terminal_encoding()
    
    # Vérification du PATH
    print("\nVérification du PATH Python...")
    check_python_path()

if __name__ == '__main__':
    main()

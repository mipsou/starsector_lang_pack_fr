#!/usr/bin/env python3
import os
import chardet
import sys
import subprocess
from datetime import datetime
import shutil
import configparser
import platform

def load_config():
    """Charge la configuration depuis le fichier approprié selon l'OS."""
    config = configparser.ConfigParser()
    
    # Détermine l'extension selon l'OS
    if platform.system() == 'Windows':
        config_files = ['tools/extract_jar.ini', 'tools/extract_jar.win.conf']
    else:
        config_files = ['tools/extract_jar.ini', 'tools/extract_jar.local.conf']
    
    # Charge les fichiers de config dans l'ordre (le dernier écrase les précédents)
    loaded = False
    for conf_file in config_files:
        if os.path.exists(conf_file):
            config.read(conf_file)
            loaded = True
    
    if not loaded:
        print(f"Erreur: Aucun fichier de configuration trouvé parmi {', '.join(config_files)}")
        sys.exit(1)
    
    if not config.has_section('7zip') or not config.has_option('7zip', 'path'):
        print("Erreur: Configuration 7zip manquante")
        sys.exit(1)
        
    return config

def check_file_encoding(file_path):
    """Vérifie l'encodage d'un fichier."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def list_jar_7z(jar_path, config):
    """Liste le contenu d'un JAR avec 7zip."""
    try:
        sevenzip = config.get('7zip', 'path')
        if not os.path.exists(sevenzip):
            print(f"Erreur: 7zip non trouvé: {sevenzip}")
            return None
            
        result = subprocess.run(
            [sevenzip, 'l', jar_path],
            capture_output=True,
            text=True,
            encoding='cp850'  # Pour Windows
        )
        if result.returncode != 0:
            print(f"Erreur 7zip: {result.stderr}")
            return None
            
        # Parse la sortie de 7zip pour extraire les noms de fichiers
        lines = result.stdout.split('\n')
        files = []
        for line in lines:
            if line.strip() and not line.startswith('--') and not line.startswith('Date'):
                parts = line.split()
                if len(parts) >= 5:
                    # Le nom du fichier est tout ce qui suit la date/heure/taille
                    name = ' '.join(parts[5:])
                    if name:
                        files.append(name)
        return files
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def extract_jar_7z(jar_path, config, extract_dir=None):
    """Extrait les fichiers de traduction d'un JAR avec 7zip."""
    if extract_dir is None:
        extract_dir = os.path.join(
            config.get('jar', 'extract_dir', fallback='jar_content'),
            os.path.basename(jar_path).replace('.jar', '')
        )
    
    # Crée le dossier d'extraction
    os.makedirs(extract_dir, exist_ok=True)
    
    # Crée un backup si demandé
    if config.getboolean('jar', 'backup', fallback=True) and os.path.exists(extract_dir) and os.listdir(extract_dir):
        date_format = config.get('jar', 'backup_date_format', fallback='%Y%m%d_%H%M%S')
        backup_dir = f"{extract_dir}_backup_{datetime.now().strftime(date_format)}"
        shutil.copytree(extract_dir, backup_dir)
        print(f"\nBackup créé: {backup_dir}")
    
    try:
        # Liste d'abord les fichiers
        files = list_jar_7z(jar_path, config)
        if not files:
            return False
            
        print("\nContenu du JAR:")
        for f in files:
            print(f"- {f}")
        
        # Extensions à extraire depuis la config
        extensions = tuple(config.get('jar', 'extensions', fallback='.json,.csv,.txt').split(','))
        
        # Identifie les fichiers de traduction
        translations = [f for f in files if f.endswith(extensions)]
        if translations:
            print("\nFichiers de traduction trouvés:")
            for f in translations:
                print(f"- {f}")
                
            # Extrait uniquement les fichiers de traduction
            sevenzip = config.get('7zip', 'path')
            for f in translations:
                result = subprocess.run(
                    [sevenzip, 'e', jar_path, f'-o{extract_dir}', f],
                    capture_output=True,
                    text=True,
                    encoding='cp850'
                )
                if result.returncode != 0:
                    print(f"Erreur lors de l'extraction de {f}: {result.stderr}")
                    return False
                    
            print(f"\nFichiers extraits dans: {extract_dir}")
        else:
            print("\nAucun fichier de traduction trouvé")
        
        return True
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def main():
    # Charge la configuration
    config = load_config()
    
    if len(sys.argv) > 1 and sys.argv[1].endswith('.jar'):
        # Mode JAR
        jar_path = sys.argv[1]
        if not os.path.exists(jar_path):
            print(f"Erreur: JAR non trouvé: {jar_path}")
            sys.exit(1)
            
        # Extrait le JAR si spécifié
        if len(sys.argv) > 2 and sys.argv[2] == '--extract':
            if extract_jar_7z(jar_path, config):
                print("\nJAR extrait avec succès")
                sys.exit(0)
            sys.exit(1)
            
        # Sinon, liste juste le contenu
        if extract_jar_7z(jar_path, config, None):
            print("\nJAR vérifié avec succès")
            sys.exit(0)
        sys.exit(1)
    
    # Mode vérification encodage
    errors = []
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith(('.json', '.csv', '.txt')):
                file_path = os.path.join(root, file)
                encoding = check_file_encoding(file_path)
                if encoding.lower() != 'utf-8':
                    errors.append(f"Erreur: {file_path} n'est pas en UTF-8 (détecté: {encoding})")
    
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("Tous les fichiers sont en UTF-8")
    sys.exit(0)

if __name__ == '__main__':
    main()

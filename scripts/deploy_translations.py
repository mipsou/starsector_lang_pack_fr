#!/usr/bin/env python3
"""
Script de déploiement des traductions
Convertit les fichiers JSON au format attendu par Starsector
"""
import json
import shutil
from pathlib import Path

def convert_to_starsector_format(input_file, output_file):
    """Convertit un fichier JSON au format Starsector"""
    # Lire le JSON source
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Créer le dossier de sortie si nécessaire
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convertir en format Starsector
    content = "{\n\ttips:[\n"
    for item in data['tips']:
        if isinstance(item, dict):
            content += f'\t{{"freq":{item["freq"]}, "tip":"{item["tip"]}"}},\n'
        else:
            content += f'\t"{item}",\n'
    
    # Retirer la dernière virgule et fermer
    content = content.rstrip(',\n') + '\n\t],\n}'
    
    # Écrire le résultat
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def main():
    """Fonction principale"""
    # Chemins des fichiers
    base_dir = Path(__file__).parent.parent
    source_dir = base_dir / 'localization' / 'fr' / 'data' / 'strings'
    deploy_dir = base_dir / 'deploy' / 'data' / 'strings'
    
    # Créer le dossier de déploiement
    deploy_dir.mkdir(parents=True, exist_ok=True)
    
    # Convertir tips.json
    tips_source = source_dir / 'tips.json'
    tips_deploy = deploy_dir / 'tips.json'
    
    print(f"Conversion de {tips_source.name}...")
    convert_to_starsector_format(tips_source, tips_deploy)
    print("Conversion terminée!")

if __name__ == '__main__':
    main()

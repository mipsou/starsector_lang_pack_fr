#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

def fix_special_chars(text):
    """Corrige les caractères spéciaux dans le texte."""
    # Table de correspondance pour les corrections
    replacements = {
        'ééé': 'é',
        'éé': 'é',
        'ééà': 'à',
        'ééâ': 'â',
        'ééè': 'è',
        'ééê': 'ê',
        'ééë': 'ë',
        'ééî': 'î',
        'ééï': 'ï',
        'ééô': 'ô',
        'ééù': 'ù',
        'ééû': 'û',
        'ééü': 'ü',
        'ééÿ': 'ÿ',
        'ééç': 'ç',
        'éÂé': 'é',
        'âÂ': 'â',
        'éÂ': 'é',
        'ééÂ': 'é',
        'manééâÂéuvre': 'manœuvre',
        'dééésengager': 'désengager',
        'empécher': 'empêcher',
        'préts': 'prêts',
        'malgrééé': 'malgré',
        'prééésence': 'présence',
        'supééérieures': 'supérieures',
        'considééérez': 'considérez',
        'déééplacent': 'déplacent',
        'éééquipage': 'équipage',
        'réééactiver': 'réactiver',
        'réééussit': 'réussit',
        'éééchapper': 'échapper',
        'éééquipes': 'équipes',
        'réééparation': 'réparation',
        'réééussi': 'réussi',
        'systééÂémes': 'systèmes',
        'opééérationnel': 'opérationnel',
        'ééétééé': 'été',
        'neutralisééé': 'neutralisé',
        'dééétruit': 'détruit',
        'dééégéÂééts': 'dégâts',
        'dééésactivant': 'désactivant',
        'durééée': 'durée',
        'préééparation': 'préparation',
        'déééploiement': 'déploiement',
        'rééécupééérer': 'récupérer',
        'nééécessaire': 'nécessaire',
        'vééérifier': 'vérifier',
        'capacitééé': 'capacité',
        'augmentééée': 'augmentée',
        'réééduite': 'réduite',
        'recommandééé': 'recommandé'
    }
    
    # Applique les corrections
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    
    # Nettoyage final
    text = text.replace('Â', '')
    text = text.replace('éé', 'é')
    
    return text

def fix_strings_json():
    """Corrige le fichier strings.json."""
    input_file = '../data/strings/strings.json'
    backup_file = '../data/strings/strings.json.bak'
    
    # Crée une sauvegarde
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"Sauvegarde créée : {backup_file}")
    
    try:
        # Lit le contenu du fichier
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Supprime les lignes vides et les commentaires
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        # Traite chaque ligne
        json_entries = {}
        for line in lines:
            if ':' in line:
                # Sépare la clé et la valeur
                key, value = line.split(':', 1)
                key = key.strip().strip('"').strip("'")
                value = value.strip().strip(',').strip()
                
                # Ignore les valeurs invalides
                if value in ['{', '}', '[', ']'] or not value:
                    continue
                
                # S'assure que la valeur est correctement formatée
                if not value.startswith('"'):
                    value = '"' + value.strip('"')
                if not value.endswith('"'):
                    value = value.strip('"') + '"'
                
                # Corrige les caractères spéciaux
                value = fix_special_chars(value)
                
                # Ajoute l'entrée au dictionnaire
                json_entries[key] = json.loads(value)
        
        # Écrit le fichier corrigé
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(json_entries, f, ensure_ascii=False, indent=4)
        
        print("Fichier strings.json corrigé avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de la correction : {str(e)}")
        # Restaure la sauvegarde en cas d'erreur
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            print("Restauration de la sauvegarde effectuée.")
        raise

if __name__ == '__main__':
    fix_strings_json()

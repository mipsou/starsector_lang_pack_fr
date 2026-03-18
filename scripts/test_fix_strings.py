#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import shutil
from fix_strings import fix_special_chars

def test_fix_strings():
    """Teste la correction sur une copie du fichier strings.json."""
    input_file = '../data/strings/strings.json'
    test_file = '../data/strings/strings.json.test'
    
    # Crée une copie pour le test
    shutil.copy2(input_file, test_file)
    print(f"Copie de test créée : {test_file}")
    
    try:
        # Lit le contenu du fichier original
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Lit le fichier de test
        with open(test_file, 'r', encoding='utf-8') as f:
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
                
                try:
                    # Teste si la valeur est du JSON valide
                    parsed_value = json.loads(value)
                    json_entries[key] = parsed_value
                except json.JSONDecodeError as e:
                    print(f"Erreur avec la clé '{key}' : {str(e)}")
                    print(f"Valeur problématique : {value}")
                    continue
        
        # Écrit le fichier de test corrigé
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(json_entries, f, ensure_ascii=False, indent=4)
        
        print("\nTest terminé ! Comparaison des fichiers :")
        print(f"Original : {input_file}")
        print(f"Corrigé  : {test_file}")
        print("\nVérifiez le fichier de test avant d'appliquer les corrections au fichier original.")
        
    except Exception as e:
        print(f"Erreur lors du test : {str(e)}")
        # Supprime le fichier de test en cas d'erreur
        if os.path.exists(test_file):
            os.remove(test_file)
            print("Fichier de test supprimé.")
        raise

if __name__ == '__main__':
    test_fix_strings()

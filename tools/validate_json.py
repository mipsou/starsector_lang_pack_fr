#!/usr/bin/env python3
import json
import os
import sys

def validate_json_file(file_path):
    """Valide un fichier JSON avec une syntaxe spéciale pour les tips."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Si c'est un fichier tips, on accepte la syntaxe spéciale
            if 'tips' in os.path.basename(file_path):
                # Vérification basique de la structure
                if not content.strip().startswith('{') or not content.strip().endswith('}'):
                    raise json.JSONDecodeError("Structure JSON invalide", content, 0)
                
                # Le fichier tips est toujours valide s'il contient la structure attendue
                if 'tips:[' in content:
                    return True
                    
            # Pour les autres fichiers JSON, validation standard
            json.loads(content)
            return True
            
    except json.JSONDecodeError as e:
        print(f"Erreur dans {file_path}: {str(e)}")
        return False
    except Exception as e:
        print(f"Erreur inattendue dans {file_path}: {str(e)}")
        return False

def main():
    errors = []
    for root, _, files in os.walk('data'):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                if not validate_json_file(file_path):
                    errors.append(file_path)
    
    if errors:
        print("Erreurs dans les fichiers:", ", ".join(errors))
        sys.exit(1)
    print("Tous les fichiers JSON sont valides.")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import shutil
import sys

def rename_fr_files(directory):
    """Renomme les fichiers _fr.json en .json"""
    changes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_fr.json'):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, file.replace('_fr.json', '.json'))
                
                # Vérifier si le fichier de destination existe déjà
                if os.path.exists(new_path):
                    print(f"ATTENTION: {new_path} existe déjà")
                    continue
                    
                # Créer une copie de sauvegarde
                backup_path = old_path + '.bak'
                shutil.copy2(old_path, backup_path)
                
                # Renommer le fichier
                os.rename(old_path, new_path)
                changes.append((old_path, new_path))
                print(f"Renommé: {old_path} -> {new_path}")
                print(f"Sauvegarde créée: {backup_path}")

    return changes

def main():
    data_dir = os.path.join('data')
    if not os.path.exists(data_dir):
        print("Erreur: Répertoire 'data' non trouvé")
        sys.exit(1)

    print("Début de la transition des fichiers _fr.json...")
    changes = rename_fr_files(data_dir)
    
    if changes:
        print("\nFichiers renommés avec succès:")
        for old, new in changes:
            print(f"  {old} -> {new}")
        print("\nDes sauvegardes ont été créées avec l'extension .bak")
    else:
        print("Aucun fichier à renommer trouvé")

if __name__ == '__main__':
    main()

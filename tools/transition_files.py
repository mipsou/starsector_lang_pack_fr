#!/usr/bin/env python3
import os
import shutil
import sys
import json
import filecmp

def compare_json_files(file1, file2):
    """Compare deux fichiers JSON"""
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            content1 = json.load(f1)
            content2 = json.load(f2)
            return content1 == content2
    except Exception as e:
        print(f"Erreur lors de la comparaison des fichiers: {str(e)}")
        return False

def check_fr_files(directory):
    """Vérifie les doublons entre fichiers _fr.json et .json"""
    duplicates = []
    for root, _, files in os.walk(directory):
        fr_files = [f for f in files if f.endswith('_fr.json')]
        for fr_file in fr_files:
            base_file = fr_file.replace('_fr.json', '.json')
            fr_path = os.path.join(root, fr_file)
            base_path = os.path.join(root, base_file)
            
            if os.path.exists(base_path):
                print(f"\nComparaison de {fr_file} avec {base_file}:")
                if filecmp.cmp(fr_path, base_path, shallow=False):
                    print("[OK] Les fichiers sont identiques (comparaison binaire)")
                    duplicates.append((fr_path, base_path))
                else:
                    try:
                        if compare_json_files(fr_path, base_path):
                            print("[OK] Les fichiers sont identiques (comparaison JSON)")
                            duplicates.append((fr_path, base_path))
                        else:
                            print("[!!] Les fichiers sont différents")
                            print("     → Vérification manuelle recommandée")
                    except Exception as e:
                        print(f"[!!] Erreur lors de la comparaison JSON: {str(e)}")
            else:
                print(f"\n{base_file} n'existe pas encore")
    
    return duplicates

def rename_fr_files(directory):
    """Renomme les fichiers _fr.json en .json"""
    # D'abord, vérifions les doublons
    duplicates = check_fr_files(directory)
    if duplicates:
        print("\nFichiers en double détectés:")
        for fr_file, base_file in duplicates:
            print(f"  {fr_file} est identique à {base_file}")
        response = input("\nDes doublons ont été trouvés. Continuer la transition ? (o/N): ")
        if response.lower() != 'o':
            print("Transition annulée")
            return []

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
                print(f"Renommé: {old_path} → {new_path}")
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
            print(f"  {old} → {new}")
        print("\nDes sauvegardes ont été créées avec l'extension .bak")
    else:
        print("Aucun fichier à renommer trouvé")

if __name__ == '__main__':
    main()

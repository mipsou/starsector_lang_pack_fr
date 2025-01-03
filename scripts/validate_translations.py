#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import sys
import os
import shutil
from pathlib import Path
import unicodedata

# Force l'encodage en UTF-8 pour la sortie
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class TranslationValidator:
    def __init__(self):
        self.base_dir = Path('D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private')
        self.translations_file = self.base_dir / 'localization/data/strings/descriptions_fr.csv'
        self.missions_dir = self.base_dir / 'localization/data/missions'
        self.validation_results = []
        
    def validate_typography(self, text):
        """Valide la typographie française"""
        issues = []
        
        # Vérification des espaces avant la ponctuation
        ponctuation_doubles = [':', '!', '?', ';', '»']
        for p in ponctuation_doubles:
            if re.search(f'[^ ]{p}', text):
                issues.append(f"Espace manquante avant '{p}'")
                
        # Vérification des espaces après la ponctuation
        if re.search(r'[,:!?;][^ ]', text):
            issues.append("Espace manquante après la ponctuation")
            
        # Vérification des points de suspension
        if re.search(r'\.{3}', text):
            issues.append("Points de suspension incorrects (utiliser …)")
            
        # Vérification des guillemets
        if re.search(r'[""]', text):
            issues.append("Guillemets droits au lieu des guillemets français « »")
            
        # Vérification des guillemets français
        if '«' in text and not re.search(r'« [^»]+» ?', text):
            issues.append("Format incorrect des guillemets français (espace après « et avant »)")
            
        return issues

    def validate_mission_text(self, mission_dir):
        """Valide le fichier mission_text.txt d'une mission"""
        text_file = mission_dir / 'mission_text.txt'
        if not text_file.exists():
            return [f"Fichier mission_text.txt manquant dans {mission_dir.name}"]
            
        issues = []
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Validation de la structure
                if not content.startswith('Lieu :'):
                    issues.append("Le fichier doit commencer par 'Lieu :'")
                
                # Validation de la typographie
                typo_issues = self.validate_typography(content)
                if typo_issues:
                    issues.extend(typo_issues)
                    
                # Validation des sections obligatoires
                required_sections = ['Date :', 'Objectifs :']
                for section in required_sections:
                    if section not in content:
                        issues.append(f"Section '{section}' manquante")
                        
                return issues
                
        except Exception as e:
            return [f"Erreur lors de la lecture du fichier : {str(e)}"]

    def validate_all_missions(self):
        """Valide tous les fichiers de mission"""
        for mission_dir in self.missions_dir.iterdir():
            if mission_dir.is_dir():
                issues = self.validate_mission_text(mission_dir)
                if issues:
                    self.validation_results.append({
                        'file': f"missions/{mission_dir.name}/mission_text.txt",
                        'issues': issues
                    })

    def validate_all(self):
        """Valide toutes les traductions"""
        self.validate_all_missions()
        
        # Affichage des résultats
        if self.validation_results:
            print("\nProblèmes de traduction trouvés :")
            for result in self.validation_results:
                print(f"\nFichier : {result['file']}")
                for issue in result['issues']:
                    print(f"  - {issue}")
        else:
            print("\nAucun problème trouvé dans les traductions.")

def load_glossary():
    """Charge le glossaire depuis le fichier."""
    glossary = {}
    glossary_path = "D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/data/glossary.csv"
    
    try:
        with open(glossary_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'en' in row and 'fr' in row:
                    glossary[row['en'].strip()] = row['fr'].strip()
    except FileNotFoundError:
        print(f"Attention : Le fichier glossaire {glossary_path} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du chargement du glossaire : {str(e)}")
    
    return glossary

def validate_mission_text(file_path):
    """Valide le format et la typographie d'un fichier mission_text.txt."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
    errors = []
    
    # Chargement du glossaire
    glossary = load_glossary()
    
    # Vérification de la structure
    if not lines or not lines[0].startswith("Lieu :"):
        errors.append("Le fichier doit commencer par 'Lieu :'")
    
    required_sections = ["Date :", "Objectifs :"]
    found_sections = set()
    
    for line in lines:
        for section in required_sections:
            if line.startswith(section):
                found_sections.add(section)
    
    missing_sections = set(required_sections) - found_sections
    for section in missing_sections:
        errors.append(f"Section manquante : {section}")
    
    # Vérification de la typographie
    double_punctuation = [";", ":", "!", "?"]
    line_number = 0
    for line in lines:
        line_number += 1
        
        # Vérification de la ponctuation
        for char in double_punctuation:
            if char in line:
                pos = line.find(char)
                if pos > 0 and line[pos-1] != ' ':
                    errors.append(f"Ligne {line_number} : Espace manquante avant '{char}'")
                if pos < len(line)-1 and line[pos+1] != ' ':
                    errors.append(f"Ligne {line_number} : Espace manquante après '{char}'")
        
        # Vérification des termes du glossaire (insensible à la casse)
        if glossary:
            for en_term, fr_term in glossary.items():
                # Recherche le terme anglais en ignorant la casse
                pattern = re.compile(re.escape(en_term), re.IGNORECASE)
                if pattern.search(line):
                    errors.append(f"Ligne {line_number} : Terme anglais '{en_term}' trouvé, utiliser '{fr_term}'")
    
    # Vérification des guillemets
    if '"' in content:
        errors.append('Utiliser les guillemets français « » au lieu de "')
    
    # Vérification des points de suspension
    if "..." in content:
        errors.append("Utiliser le caractère points de suspension (…) au lieu de ...")
    
    return errors

def auto_correct_text(content, glossary):
    """Corrige automatiquement le texte selon les règles typographiques et le glossaire."""
    # Correction des espaces avant/après la ponctuation
    double_punctuation = [";", ":", "!", "?"]
    for char in double_punctuation:
        # Ajoute l'espace avant
        content = content.replace(f"{char}", f" {char}")
        # Supprime les espaces multiples
        content = content.replace(f"  {char}", f" {char}")
        # Ajoute l'espace après
        content = content.replace(f"{char}", f"{char} ")
        # Supprime les espaces multiples
        content = content.replace(f"{char}  ", f"{char} ")
    
    # Correction des guillemets
    content = content.replace('"', "« ")
    content = content.replace('"', " »")
    
    # Correction des points de suspension
    content = content.replace("...", "…")
    
    # Correction des termes du glossaire (insensible à la casse)
    if glossary:
        for en_term, fr_term in glossary.items():
            pattern = re.compile(re.escape(en_term), re.IGNORECASE)
            content = pattern.sub(fr_term, content)
    
    return content

def create_backup(file_path):
    """Crée une sauvegarde du fichier."""
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    return backup_path

def auto_correct_file(file_path):
    """Corrige automatiquement un fichier en créant une sauvegarde."""
    # Crée une sauvegarde avant modification
    backup_path = create_backup(file_path)
    
    # Charge le contenu du fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Applique les corrections
    glossary = load_glossary()
    corrected = auto_correct_text(content, glossary)
    
    # Écrit le contenu corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(corrected)
    
    return backup_path

def validate_and_correct_mission_text(file_path):
    """Valide et corrige le fichier mission_text.txt."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chargement du glossaire
    glossary = load_glossary()
    
    # Validation
    errors = validate_mission_text(file_path)
    
    if errors:
        print("\nErreurs trouvées :")
        for error in errors:
            print(f"  - {error}")
        
        # Correction automatique
        corrected_content = auto_correct_text(content, glossary)
        
        if corrected_content != content:
            backup_path = create_backup(file_path)
            print(f"\nCréation d'une sauvegarde : {backup_path}")
            
            print("Application des corrections automatiques...")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            
            # Validation après correction
            new_errors = validate_mission_text(file_path)
            if new_errors:
                print("\nErreurs restantes après correction :")
                for error in new_errors:
                    print(f"  - {error}")
            else:
                print("\nToutes les erreurs ont été corrigées.")
    else:
        print("Aucune erreur trouvée.")

def main():
    """Point d'entrée principal du script."""
    mission_dir = "D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/data/missions"
    
    if not os.path.exists(mission_dir):
        print(f"Erreur : Le répertoire {mission_dir} n'existe pas.")
        return
    
    print("Validation des fichiers de mission...")
    has_errors = False
    
    for root, dirs, files in os.walk(mission_dir):
        for file in files:
            if file == "mission_text.txt":
                file_path = os.path.join(root, file)
                mission_name = os.path.basename(os.path.dirname(file_path))
                
                print(f"\nValidation de la mission : {mission_name}")
                try:
                    validate_and_correct_mission_text(file_path)
                except Exception as e:
                    has_errors = True
                    print(f"Erreur lors de la validation : {str(e)}")

    if not has_errors:
        print("\nAucune erreur trouvée dans les fichiers de mission.")
    else:
        print("\nDes erreurs ont été trouvées. Veuillez les corriger.")

if __name__ == '__main__':
    main()

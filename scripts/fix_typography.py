#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path
import shutil

class TypographyFixer:
    def __init__(self):
        self.base_dir = Path('D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private')
        self.missions_dir = self.base_dir / 'localization/data/missions'
        self.backup_dir = self.base_dir / 'backups/missions'
        
    def create_backup(self, file_path):
        """Crée une sauvegarde du fichier avant modification"""
        backup_path = self.backup_dir / file_path.relative_to(self.missions_dir)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        print(f"Sauvegarde créée : {backup_path}")
        
    def fix_typography(self, text):
        """Corrige la typographie française dans le texte"""
        # Points de suspension
        text = re.sub(r'\.{3}', '…', text)
        
        # Espaces avant la ponctuation double
        text = re.sub(r'([^ ])([:!?;])', r'\1 \2', text)
        
        # Guillemets français
        text = re.sub(r'"([^"]+)"', r'« \1 »', text)
        
        # Structure du fichier mission
        if not text.startswith('Lieu :'):
            text = text.replace('Location:', 'Lieu :')
            
        if 'Date:' in text:
            text = text.replace('Date:', 'Date :')
            
        return text
        
    def fix_mission_file(self, mission_dir):
        """Corrige la typographie dans un fichier mission_text.txt"""
        text_file = mission_dir / 'mission_text.txt'
        if not text_file.exists():
            print(f"Fichier manquant : {text_file}")
            return
            
        try:
            # Lecture du fichier
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Création de la sauvegarde
            self.create_backup(text_file)
            
            # Correction de la typographie
            fixed_content = self.fix_typography(content)
            
            # Écriture du fichier corrigé
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
                
            print(f"Fichier corrigé : {text_file}")
            
        except Exception as e:
            print(f"Erreur lors du traitement de {text_file} : {str(e)}")
            
    def fix_all_missions(self):
        """Corrige la typographie dans tous les fichiers mission"""
        print("Début de la correction typographique...")
        
        # Création du dossier de sauvegarde
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Traitement de chaque mission
        for mission_dir in self.missions_dir.iterdir():
            if mission_dir.is_dir():
                print(f"\nTraitement de la mission : {mission_dir.name}")
                self.fix_mission_file(mission_dir)
                
        print("\nCorrection typographique terminée !")

def main():
    fixer = TypographyFixer()
    fixer.fix_all_missions()

if __name__ == '__main__':
    main()

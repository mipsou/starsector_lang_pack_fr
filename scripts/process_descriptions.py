import csv
import os
from pathlib import Path
import codecs
import re

class DescriptionProcessor:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.descriptions_file = self.base_path / 'localization/data/strings/descriptions.csv'
        self.chunks_dir = self.base_path / 'temp/description_chunks'
        self.processed_dir = self.base_path / 'temp/processed_chunks'
        self.chunk_size = 1000
        self.encoding = 'utf-8'
        
        # Dictionnaire de traduction pour les termes techniques
        self.tech_terms = {
            'Shield': 'Bouclier',
            'Hull': 'Coque',
            'Armor': 'Blindage',
            'Flux': 'Flux',
            'Weapon': 'Arme',
            'System': 'Système',
            'Damage': 'Dégâts',
            'Speed': 'Vitesse',
            'Range': 'Portée',
            'Capacity': 'Capacité',
            'Energy': 'Énergie',
            'Ballistic': 'Balistique',
            'Missile': 'Missile',
            'Fighter': 'Chasseur',
            'Carrier': 'Porte-vaisseaux',
            'Combat': 'Combat',
            'Defense': 'Défense',
            'Attack': 'Attaque',
            'Power': 'Puissance',
            'Efficiency': 'Efficacité',
            'Point defense': 'Point de défense',
            'Destroyer': 'Destroyer',
            'Cruiser': 'Croiseur',
            'Battleship': 'Cuirassé',
            'Frigate': 'Frégate',
            'Engine': 'Moteur',
            'Core': 'Noyau',
            'System': 'Système',
            'Weapon': 'Arme',
            'Shield': 'Bouclier',
            'Hull': 'Coque',
            'Armor': 'Blindage',
            'Flux': 'Flux',
            'Damage': 'Dégâts',
            'Speed': 'Vitesse',
            'Range': 'Portée',
            'Capacity': 'Capacité',
            'Energy': 'Énergie',
            'Ballistic': 'Balistique',
            'Strike': 'Frappe',
            'Support': 'Soutien',
            'Command': 'Commandement',
            'Phase': 'Phase',
            'Jump': 'Saut',
            'Drive': 'Propulsion',
            'Reactor': 'Réacteur',
            'Generator': 'Générateur',
            'Computer': 'Ordinateur',
            'Sensor': 'Capteur',
            'Scanner': 'Scanner',
            'Targeting': 'Ciblage',
            'Navigation': 'Navigation',
            'Communication': 'Communication',
            'Assault': 'Assaut',
            'Task': 'Tâche',
            'Orders': 'Ordres',
            'Assignment': 'Mission',
            'Defend': 'Défendre',
            'Attack': 'Attaquer',
            'Move': 'Déplacer',
            'Hold': 'Tenir',
            'Retreat': 'Retraiter',
            'Engage': 'Engager',
            'Disengage': 'Désengager',
            'Deploy': 'Déployer',
            'Recall': 'Rappeler',
            'Guard': 'Garder',
            'Escort': 'Escorter',
            'Search': 'Rechercher',
            'Patrol': 'Patrouiller',
            'Intercept': 'Intercepter',
            'Assist': 'Assister',
            'Eliminate': 'Éliminer'
        }
        
        # Dictionnaire des genres
        self.word_genders = {
            'ship': 'le',
            'weapon': 'l\'',
            'system': 'le',
            'shield': 'le',
            'hull': 'la',
            'armor': 'le',
            'fleet': 'la',
            'missile': 'le',
            'fighter': 'le',
            'carrier': 'le',
            'destroyer': 'le',
            'cruiser': 'le',
            'battleship': 'le',
            'frigate': 'la',
            'engine': 'le',
            'core': 'le',
            'generator': 'le',
            'computer': 'l\'',
            'sensor': 'le',
            'scanner': 'le',
            'reactor': 'le',
            'drive': 'le',
            'weapon': 'l\'',
            'defense': 'la',
            'attack': 'l\'',
            'power': 'la',
            'efficiency': 'l\'',
            'capacity': 'la',
            'energy': 'l\'',
            'damage': 'les',
            'speed': 'la',
            'range': 'la'
        }
        
        # Création des répertoires nécessaires
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def get_article(self, word):
        """Détermine l'article approprié pour un mot"""
        word = word.lower()
        for key, article in self.word_genders.items():
            if word.startswith(key.lower()):
                return article
        return 'le'  # Article par défaut

    def translate_text(self, text):
        """Traduit un texte en appliquant les règles de traduction"""
        if not text:
            return text
            
        # Remplacement des termes techniques
        for eng, fr in self.tech_terms.items():
            pattern = re.compile(r'\b' + re.escape(eng) + r'\b', re.IGNORECASE)
            text = pattern.sub(lambda m: fr if m.group().isupper() else fr.lower(), text)
        
        # Correction des articles avec gestion du genre
        text = re.sub(r'\ba\s+([aeiouAEIOUhH])', r'un \1', text)  # "a" devant voyelle
        text = re.sub(r'\ba\s+([^aeiouAEIOUhH])', r'un \1', text)  # "a" devant consonne
        
        # Remplacement de "the" avec le bon article selon le genre
        def replace_the(match):
            word = match.group(1)
            article = self.get_article(word)
            return f"{article} {word}"
        
        text = re.sub(r'\bthe\s+(\w+)', replace_the, text, flags=re.IGNORECASE)
        
        # Correction de la ponctuation française
        ESPACE_FINE = chr(0x202F)  # Espace fine insécable
        text = text.replace(' !', ESPACE_FINE + '!')
        text = text.replace(' ?', ESPACE_FINE + '?')
        text = text.replace(' :', ESPACE_FINE + ':')
        text = text.replace(' ;', ESPACE_FINE + ';')
        text = text.replace('...', '…')
        
        # Correction des guillemets
        text = text.replace('"', '«' + ESPACE_FINE).replace('"', ESPACE_FINE + '»')
        
        # Correction des espaces avant les unités
        def add_fine_space(match):
            return match.group(1) + ESPACE_FINE + match.group(2)
        
        text = re.sub(r'(\d+)\s*(km|m|cm|mm|kg|g|s|min|h)', add_fine_space, text)
        
        return text

    def convert_to_utf8(self, file_path):
        """Convertit un fichier en UTF-8"""
        print(f"Conversion du fichier en UTF-8 : {file_path}")
        
        encodings = ['cp1252', 'latin1', 'utf-8-sig', 'utf-8', 'iso-8859-1']
        content = None
        detected_encoding = None
        
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                    detected_encoding = enc
                    print(f"Fichier lu avec succès en {enc}")
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise ValueError("Impossible de détecter l'encodage du fichier")
        
        backup_path = file_path.parent / (file_path.name + '.bak')
        if not backup_path.exists():
            import shutil
            shutil.copy2(file_path, backup_path)
            print(f"Backup créé : {backup_path}")
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        
        print(f"Fichier converti en UTF-8 (encodage d'origine : {detected_encoding})")
        return True

    def split_descriptions(self):
        """Divise le fichier descriptions.csv en chunks plus petits"""
        print(f"Découpage du fichier descriptions.csv...")
        
        self.convert_to_utf8(self.descriptions_file)
        
        try:
            with open(self.descriptions_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                chunk = []
                chunk_num = 0
                
                for row in reader:
                    chunk.append(row)
                    
                    if len(chunk) >= self.chunk_size:
                        self._write_chunk(chunk, header, chunk_num)
                        chunk = []
                        chunk_num += 1
                
                if chunk:
                    self._write_chunk(chunk, header, chunk_num)
            
            print("Découpage terminé avec succès")
            
        except Exception as e:
            print(f"Erreur lors du traitement : {str(e)}")
            raise

    def _write_chunk(self, chunk, header, chunk_num):
        """Écrit un chunk dans un fichier"""
        chunk_file = self.chunks_dir / f'descriptions_chunk_{chunk_num}.csv'
        
        with open(chunk_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(chunk)
            
        print(f"Chunk {chunk_num} créé : {chunk_file}")

    def process_chunk(self, chunk_file):
        """Traite un chunk de descriptions"""
        print(f"Traitement du chunk : {chunk_file}")
        
        processed_rows = []
        with open(chunk_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            for row in reader:
                # Traduction du texte tout en préservant la structure
                translated_row = []
                for i, cell in enumerate(row):
                    # On traduit uniquement les colonnes de texte
                    if i in [0, 2]:  # nom et description
                        translated_row.append(self.translate_text(cell))
                    else:
                        translated_row.append(cell)
                processed_rows.append(translated_row)
        
        output_file = self.processed_dir / chunk_file.name
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(processed_rows)
            
        print(f"Chunk traité sauvegardé : {output_file}")

    def merge_processed_chunks(self):
        """Fusionne tous les chunks traités en un seul fichier"""
        print("Fusion des chunks traités...")
        
        output_file = self.base_path / 'localization/data/strings/descriptions_fr.csv'
        first_chunk = True
        
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            
            for chunk_file in sorted(self.processed_dir.glob('*.csv')):
                with open(chunk_file, 'r', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    header = next(reader)
                    
                    if first_chunk:
                        writer.writerow(header)
                        first_chunk = False
                    
                    for row in reader:
                        writer.writerow(row)
        
        print(f"Fusion terminée : {output_file}")

def main():
    base_path = "D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private"
    processor = DescriptionProcessor(base_path)
    
    try:
        processor.split_descriptions()
        
        for chunk_file in sorted(processor.chunks_dir.glob('*.csv')):
            processor.process_chunk(chunk_file)
        
        processor.merge_processed_chunks()
        
        print("Traitement terminé avec succès !")
    except Exception as e:
        print(f"Erreur lors du traitement : {str(e)}")
        raise

if __name__ == '__main__':
    main()

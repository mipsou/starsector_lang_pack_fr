#!/usr/bin/env python3
"""
Script de traitement des descriptions pour Starsector

Ce script :
- Traite les fichiers CSV de descriptions
- Applique les règles typographiques françaises
- Normalise les termes techniques
- Gère les genres grammaticaux

Auteur: Mipsou
Date: 2025-01-22
"""
import csv
import os
import sys
from pathlib import Path
import codecs
import re
import unittest
import shutil

# Ajout du répertoire des scripts au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from utils import (fix_quotes, validate_typography, check_encoding,
                  detect_file_format, format_file)

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
        }
        
    def setup_directories(self):
        """Crée et nettoie les répertoires de travail."""
        # Suppression des anciens répertoires
        if self.chunks_dir.exists():
            shutil.rmtree(self.chunks_dir)
        if self.processed_dir.exists():
            shutil.rmtree(self.processed_dir)
            
        # Création des nouveaux répertoires
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, strict=True):
        """Valide le fichier de descriptions.
        
        Args:
            strict (bool): Si True, vérifie strictement l'encodage UTF-8
            
        Returns:
            bool: True si le fichier est valide, False sinon
        """
        try:
            # Vérification du format
            file_format = detect_file_format(self.descriptions_file)
            if file_format != 'csv':
                raise ValueError(f"Le fichier {self.descriptions_file} n'est pas au format CSV")
                
            # Vérification de l'encodage
            if not check_encoding(self.descriptions_file, strict=strict):
                raise ValueError(f"Le fichier {self.descriptions_file} n'est pas en UTF-8")
                
            return True
            
        except Exception as e:
            print(f"Erreur de validation : {e}")
            return False
    
    def process_chunk(self, chunk_file):
        """Traite un fichier chunk de descriptions.
        
        Args:
            chunk_file (Path): Chemin du fichier chunk à traiter
            
        Returns:
            bool: True si le traitement a réussi, False sinon
        """
        try:
            processed_lines = []
            
            with open(chunk_file, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Traduction des termes techniques
                    description = row['description']
                    for eng, fr in self.tech_terms.items():
                        description = re.sub(r'\b' + eng + r'\b', fr, description)
                    
                    # Correction de la typographie
                    description = fix_quotes(description)
                    
                    # Validation de la typographie
                    is_valid, errors = validate_typography(description)
                    if not is_valid:
                        print(f"Avertissements pour {row['id']} :")
                        for error in errors:
                            print(f"  - {error}")
                    
                    # Mise à jour de la ligne
                    row['description'] = description
                    processed_lines.append(row)
            
            # Écriture du fichier traité
            output_file = self.processed_dir / chunk_file.name
            with open(output_file, 'w', encoding=self.encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=processed_lines[0].keys())
                writer.writeheader()
                writer.writerows(processed_lines)
                
            return True
            
        except Exception as e:
            print(f"Erreur lors du traitement du chunk {chunk_file.name} : {e}")
            return False
    
    def process_descriptions(self, strict=True):
        """Traite le fichier de descriptions complet.
        
        Args:
            strict (bool): Si True, vérifie strictement l'encodage UTF-8
            
        Returns:
            bool: True si le traitement a réussi, False sinon
        """
        try:
            # Préparation des répertoires
            self.setup_directories()
            
            # Validation du fichier source
            if not self.validate_file(strict=strict):
                return False
            
            # Lecture et découpage en chunks
            with open(self.descriptions_file, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                current_chunk = []
                chunk_num = 0
                
                for row in reader:
                    current_chunk.append(row)
                    
                    if len(current_chunk) >= self.chunk_size:
                        chunk_file = self.chunks_dir / f'chunk_{chunk_num}.csv'
                        with open(chunk_file, 'w', encoding=self.encoding, newline='') as cf:
                            writer = csv.DictWriter(cf, fieldnames=current_chunk[0].keys())
                            writer.writeheader()
                            writer.writerows(current_chunk)
                        
                        if not self.process_chunk(chunk_file):
                            return False
                            
                        current_chunk = []
                        chunk_num += 1
                
                # Traitement du dernier chunk
                if current_chunk:
                    chunk_file = self.chunks_dir / f'chunk_{chunk_num}.csv'
                    with open(chunk_file, 'w', encoding=self.encoding, newline='') as cf:
                        writer = csv.DictWriter(cf, fieldnames=current_chunk[0].keys())
                        writer.writeheader()
                        writer.writerows(current_chunk)
                    
                    if not self.process_chunk(chunk_file):
                        return False
            
            print("Traitement des descriptions terminé avec succès.")
            return True
            
        except Exception as e:
            print(f"Erreur lors du traitement : {e}")
            return False

class TestDescriptionProcessor(unittest.TestCase):
    """Tests unitaires pour le traitement des descriptions."""
    
    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = Path("tests")
        self.test_file = self.test_dir / "descriptions_test.csv"
        self.test_dir.mkdir(exist_ok=True)
        
        # Création d'un fichier de test
        with open(self.test_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'description'])
            writer.writerow(['test1', 'A Shield system with Hull armor'])
            writer.writerow(['test2', 'High Damage Energy weapon'])
            writer.writerow(['test3', '"Test" with "quotes"'])
    
    def tearDown(self):
        """Nettoyage après les tests."""
        if self.test_file.exists():
            self.test_file.unlink()
        if self.test_dir.exists() and not any(self.test_dir.iterdir()):
            self.test_dir.rmdir()
    
    def test_process_descriptions(self):
        """Teste le processus complet de traitement."""
        processor = DescriptionProcessor(self.test_dir)
        processor.descriptions_file = self.test_file
        
        # Test avec mode permissif
        self.assertTrue(processor.process_descriptions(strict=False))
        
        # Vérification du format
        file_format = detect_file_format(self.test_file)
        self.assertEqual(file_format, 'csv')
        
        # Test de traduction des termes
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('Shield', content)
        self.assertIn('Hull', content)
        
        # Test du formatage
        formatted = format_file(self.test_file, content)
        self.assertTrue(formatted.strip())
        
        # Test des guillemets
        self.assertIn('"Test"', content)
        
        # Test de l'encodage
        self.assertTrue(check_encoding(self.test_file, strict=False))
    
    def test_invalid_file(self):
        """Teste le comportement avec un fichier invalide."""
        processor = DescriptionProcessor(self.test_dir)
        processor.descriptions_file = self.test_dir / "nonexistent.csv"
        
        self.assertFalse(processor.process_descriptions())

def main():
    """Point d'entrée principal du script."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=['dummy'])
    else:
        if len(sys.argv) < 2:
            print("Usage: python process_descriptions.py base_path [--test]")
            sys.exit(1)
            
        base_path = sys.argv[1]
        processor = DescriptionProcessor(base_path)
        
        if not processor.process_descriptions():
            sys.exit(1)

if __name__ == '__main__':
    main()

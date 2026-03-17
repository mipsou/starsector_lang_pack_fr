#!/usr/bin/env python3
"""
Script de traitement des images pour la traduction.
Permet d'extraire le texte des images, de le traduire et de générer de nouvelles images.
"""

import os
import json
import logging
from pathlib import Path
from PIL import Image
import pytesseract
from typing import Dict, List, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_processing.log'),
        logging.StreamHandler()
    ]
)

class ImageProcessor:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.processed_images: Dict[str, Dict] = {}
        
    def process_all(self) -> bool:
        """Traite toutes les images dans le répertoire source."""
        try:
            # Création du répertoire cible s'il n'existe pas
            self.target_dir.mkdir(parents=True, exist_ok=True)
            
            # Parcours des images
            for img_path in self.source_dir.rglob('*'):
                if img_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    self._process_image(img_path)
            
            # Sauvegarde du rapport
            self._save_report()
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement des images : {str(e)}")
            return False
    
    def _process_image(self, img_path: Path) -> None:
        """Traite une image individuelle."""
        try:
            # Chargement de l'image
            img = Image.open(img_path)
            
            # Extraction du texte
            text = pytesseract.image_to_string(img, lang='eng')
            
            # Enregistrement des informations
            rel_path = img_path.relative_to(self.source_dir)
            self.processed_images[str(rel_path)] = {
                'original_path': str(img_path),
                'extracted_text': text.strip(),
                'status': 'processed',
                'type': self._determine_image_type(img_path, text)
            }
            
            logging.info(f"Image traitée : {rel_path}")
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement de {img_path}: {str(e)}")
            self.processed_images[str(img_path)] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _determine_image_type(self, img_path: Path, text: str) -> str:
        """Détermine le type d'image basé sur son emplacement et contenu."""
        path_str = str(img_path).lower()
        
        if 'button' in path_str or len(text) < 20:
            return 'button'
        elif 'interface' in path_str:
            return 'interface'
        elif text and len(text) > 100:
            return 'text'
        else:
            return 'unknown'
    
    def _save_report(self) -> None:
        """Sauvegarde le rapport de traitement."""
        report_path = self.target_dir / 'image_processing_report.json'
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.processed_images, f, ensure_ascii=False, indent=2)
            logging.info(f"Rapport sauvegardé : {report_path}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde du rapport : {str(e)}")

def main():
    """Point d'entrée principal."""
    import argparse
    parser = argparse.ArgumentParser(
        description='Traite les images pour la traduction.'
    )
    parser.add_argument(
        'source_dir',
        help='Répertoire source contenant les images originales'
    )
    parser.add_argument(
        'target_dir',
        help='Répertoire cible pour les images traitées'
    )
    args = parser.parse_args()
    
    processor = ImageProcessor(args.source_dir, args.target_dir)
    success = processor.process_all()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())

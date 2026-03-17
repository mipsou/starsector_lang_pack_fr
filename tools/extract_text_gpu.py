#!/usr/bin/env python3
"""
Script d'extraction de texte optimisé pour GPU via WSL2 et ROCm.
Utilise PyTorch avec backend ROCm pour l'accélération GPU.
"""

import os
import json
import logging
import torch
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gpu_extraction.log'),
        logging.StreamHandler()
    ]
)

class GPUTextExtractor:
    def __init__(self, device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialise l'extracteur de texte avec support GPU."""
        self.device = device
        logging.info(f"Utilisation du périphérique : {device}")
        
        # Vérification de ROCm
        if torch.cuda.is_available():
            if 'rocm' in torch.version.hip:
                logging.info("ROCm détecté et actif")
            else:
                logging.warning("CUDA détecté mais pas ROCm")
        
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Prétraite l'image pour l'extraction de texte."""
        # Conversion en niveaux de gris
        if image.mode != 'L':
            image = image.convert('L')
        
        # Normalisation et conversion en tensor
        img_array = np.array(image) / 255.0
        tensor = torch.from_numpy(img_array).float()
        tensor = tensor.unsqueeze(0).unsqueeze(0)  # Ajout des dimensions batch et channel
        
        return tensor.to(self.device)
    
    def detect_text_regions(self, tensor: torch.Tensor) -> List[Tuple[int, int, int, int]]:
        """Détecte les régions contenant du texte dans l'image."""
        # TODO: Implémenter la détection de texte avec un modèle CNN
        # Pour l'instant, retourne toute l'image comme région
        h, w = tensor.shape[-2:]
        return [(0, 0, w, h)]
    
    def extract_text(self, image_path: str) -> Dict[str, any]:
        """Extrait le texte d'une image avec accélération GPU."""
        try:
            # Chargement et prétraitement
            image = Image.open(image_path)
            tensor = self.preprocess_image(image)
            
            # Détection des régions de texte
            regions = self.detect_text_regions(tensor)
            
            # Préparation du résultat
            result = {
                'path': image_path,
                'regions': regions,
                'status': 'success',
                'device': self.device
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement de {image_path}: {str(e)}")
            return {
                'path': image_path,
                'status': 'error',
                'error': str(e)
            }
    
    def batch_process(self, image_dir: str, batch_size: int = 4) -> Dict[str, List[Dict]]:
        """Traite un lot d'images en parallèle."""
        results = {
            'success': [],
            'error': []
        }
        
        try:
            # Parcours des images par lots
            image_paths = [
                str(p) for p in Path(image_dir).rglob('*')
                if p.suffix.lower() in ['.png', '.jpg', '.jpeg']
            ]
            
            for i in range(0, len(image_paths), batch_size):
                batch = image_paths[i:i + batch_size]
                for img_path in batch:
                    result = self.extract_text(img_path)
                    if result['status'] == 'success':
                        results['success'].append(result)
                    else:
                        results['error'].append(result)
                
                logging.info(f"Traité {min(i + batch_size, len(image_paths))}/{len(image_paths)} images")
            
            return results
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement par lots : {str(e)}")
            return results

def main():
    """Point d'entrée principal."""
    import argparse
    parser = argparse.ArgumentParser(
        description='Extrait le texte des images avec accélération GPU.'
    )
    parser.add_argument(
        'image_dir',
        help='Répertoire contenant les images à traiter'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=4,
        help='Taille des lots pour le traitement parallèle'
    )
    args = parser.parse_args()
    
    extractor = GPUTextExtractor()
    results = extractor.batch_process(args.image_dir, args.batch_size)
    
    # Sauvegarde des résultats
    output_file = 'extraction_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logging.info(f"Résultats sauvegardés dans {output_file}")
    
    return 0 if len(results['success']) > 0 else 1

if __name__ == "__main__":
    exit(main())

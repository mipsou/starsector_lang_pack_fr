#!/usr/bin/env python3
"""
Tests unitaires pour l'extracteur de texte GPU.
"""

import unittest
import os
import json
from pathlib import Path
import tempfile
import shutil
import torch
import numpy as np
from PIL import Image
from extract_text_gpu import GPUTextExtractor

class TestGPUTextExtractor(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        self.image_dir = Path(self.test_dir) / "images"
        self.image_dir.mkdir()
        
        # Création d'images de test
        self._create_test_images()
        
        # Initialisation de l'extracteur
        self.extractor = GPUTextExtractor()
    
    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)
    
    def _create_test_images(self):
        """Crée des images de test avec différentes caractéristiques."""
        # Image simple en noir et blanc
        bw_img = np.zeros((100, 200), dtype=np.uint8)
        bw_img[25:75, 50:150] = 255  # Rectangle blanc
        bw_path = self.image_dir / "bw_test.png"
        Image.fromarray(bw_img).save(bw_path)
        
        # Image en couleur
        color_img = np.zeros((200, 300, 3), dtype=np.uint8)
        color_img[50:150, 100:200] = [255, 255, 255]  # Rectangle blanc
        color_path = self.image_dir / "color_test.png"
        Image.fromarray(color_img).save(color_path)
    
    def test_device_selection(self):
        """Test de la sélection du périphérique."""
        self.assertIn(self.extractor.device, ['cuda', 'cpu'])
    
    def test_preprocess_image(self):
        """Test du prétraitement des images."""
        # Test avec image noir et blanc
        bw_path = self.image_dir / "bw_test.png"
        image = Image.open(bw_path)
        tensor = self.extractor.preprocess_image(image)
        
        self.assertIsInstance(tensor, torch.Tensor)
        self.assertEqual(len(tensor.shape), 4)  # [batch, channel, height, width]
        self.assertEqual(tensor.device.type, self.extractor.device)
    
    def test_batch_processing(self):
        """Test du traitement par lots."""
        results = self.extractor.batch_process(str(self.image_dir), batch_size=2)
        
        self.assertIsInstance(results, dict)
        self.assertIn('success', results)
        self.assertIn('error', results)
        self.assertGreater(len(results['success']), 0)
    
    def test_error_handling(self):
        """Test de la gestion des erreurs."""
        # Test avec un fichier invalide
        invalid_path = self.image_dir / "invalid.txt"
        invalid_path.touch()
        
        result = self.extractor.extract_text(str(invalid_path))
        self.assertEqual(result['status'], 'error')
        self.assertIn('error', result)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Tests unitaires pour le processeur d'images.
"""

import unittest
import os
import json
from pathlib import Path
import tempfile
import shutil
from PIL import Image
import numpy as np
from process_images import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = Path(self.test_dir) / "source"
        self.target_dir = Path(self.test_dir) / "target"
        self.source_dir.mkdir()
        
        # Création d'images de test
        self._create_test_images()
    
    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)
    
    def _create_test_images(self):
        """Crée des images de test avec du texte."""
        # Image de bouton
        button_img = np.zeros((100, 200, 3), dtype=np.uint8)
        button_img.fill(255)
        button_path = self.source_dir / "button.png"
        Image.fromarray(button_img).save(button_path)
        
        # Image d'interface
        interface_img = np.zeros((400, 600, 3), dtype=np.uint8)
        interface_img.fill(200)
        interface_path = self.source_dir / "interface" / "menu.png"
        interface_path.parent.mkdir(exist_ok=True)
        Image.fromarray(interface_img).save(interface_path)
    
    def test_process_images(self):
        """Test du traitement des images."""
        processor = ImageProcessor(str(self.source_dir), str(self.target_dir))
        success = processor.process_all()
        
        self.assertTrue(success)
        self.assertTrue((self.target_dir / 'image_processing_report.json').exists())
        
        # Vérification du rapport
        with open(self.target_dir / 'image_processing_report.json', 'r') as f:
            report = json.load(f)
            self.assertGreater(len(report), 0)
            
            # Vérification des types d'images
            button_found = False
            interface_found = False
            for img_info in report.values():
                if img_info['type'] == 'button':
                    button_found = True
                elif img_info['type'] == 'interface':
                    interface_found = True
            
            self.assertTrue(button_found)
            self.assertTrue(interface_found)
    
    def test_error_handling(self):
        """Test de la gestion des erreurs."""
        # Test avec un répertoire source inexistant
        processor = ImageProcessor(
            "repertoire_inexistant",
            str(self.target_dir)
        )
        success = processor.process_all()
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()

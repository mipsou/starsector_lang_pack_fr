#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests unitaires pour l'extracteur de JAR.
"""

import os
import tempfile
import unittest
from pathlib import Path
from jar_extractor import JarExtractor

class TestJarExtractor(unittest.TestCase):
    def setUp(self):
        """Prépare l'environnement de test."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_jar = Path(self.temp_dir) / "test.jar"
        self.output_dir = Path(self.temp_dir) / "output"
        
    def tearDown(self):
        """Nettoie l'environnement après les tests."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_create_backup(self):
        """Teste la création de backup."""
        # Créer un faux JAR pour le test
        with open(self.test_jar, 'wb') as f:
            f.write(b'test content')
            
        extractor = JarExtractor(self.test_jar, self.output_dir)
        self.assertTrue(extractor.create_backup())
        
        # Vérifier que le backup existe
        backup_files = list(Path(self.output_dir / "backups").glob("**/test.jar"))
        self.assertEqual(len(backup_files), 1)
        
    def test_calculate_hash(self):
        """Teste le calcul de hash."""
        # Créer un fichier test
        test_file = Path(self.temp_dir) / "test.txt"
        with open(test_file, 'wb') as f:
            f.write(b'test content')
            
        extractor = JarExtractor(self.test_jar, self.output_dir)
        hash1 = extractor.calculate_hash(test_file)
        
        # Vérifier que le même contenu donne le même hash
        with open(test_file, 'wb') as f:
            f.write(b'test content')
        hash2 = extractor.calculate_hash(test_file)
        
        self.assertEqual(hash1, hash2)
        
        # Vérifier qu'un contenu différent donne un hash différent
        with open(test_file, 'wb') as f:
            f.write(b'different content')
        hash3 = extractor.calculate_hash(test_file)
        
        self.assertNotEqual(hash1, hash3)

if __name__ == '__main__':
    unittest.main()

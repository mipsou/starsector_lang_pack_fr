#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests unitaires pour les utilitaires du système de traduction.
Organisation basée sur le modèle de test_rebuild.py pour une meilleure cohérence.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import logging
import logging.handlers
from pathlib import Path

# Ajout du répertoire parent au PYTHONPATH
SCRIPT_DIR = Path(__file__).parent.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from utils.logging_utils import setup_logger, LogConfig
from utils.path_utils import PathManager
from utils.binary_utils import find_control_chars_binary

class TestUtils(unittest.TestCase):
    """Tests unifiés pour tous les utilitaires."""
    
    def setUp(self):
        """Initialisation commune pour tous les tests."""
        # Crée un répertoire temporaire pour les tests
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_dir / "path_tests"
        self.test_dir.mkdir(parents=True)
        
        # Configure le logger de test
        self.log_config = LogConfig(
            log_dir=str(self.temp_dir),
            name="test_logger"
        )
        self.logger = None
        
        # Configure le gestionnaire de chemins
        self.path_manager = PathManager(str(self.test_dir))
        
        # Configuration pour les tests binaires
        self.binary_test_dir = self.temp_dir / "binary_tests"
        self.binary_test_dir.mkdir(parents=True)
        
    def tearDown(self):
        """Nettoyage commun après tous les tests."""
        if self.logger:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                handler.close()
        shutil.rmtree(self.temp_dir)
    
    # Tests des utilitaires de logging
    def test_logger_creation(self):
        """Teste la création d'un logger."""
        self.logger = setup_logger("test_logger", config=self.log_config)
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.name, "test_logger")
    
    def test_log_file_creation(self):
        """Teste la création du fichier de log."""
        self.logger = setup_logger("test_logger", config=self.log_config)
        self.logger.info("Test message")
        log_file = self.temp_dir / "test_logger.log"
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("Test message", content)
    
    def test_log_rotation(self):
        """Teste la rotation des fichiers de log."""
        self.logger = setup_logger("test_logger", config=self.log_config)
        # Configure une taille maximale plus petite pour forcer la rotation
        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.maxBytes = 1024  # 1 Ko
        
        # Génère suffisamment de logs pour déclencher la rotation
        for _ in range(100):
            self.logger.info("X" * 100)
            
        # Force la fermeture des handlers pour s'assurer que les fichiers sont écrits
        for handler in self.logger.handlers:
            handler.close()
            
        # Vérifie qu'au moins un fichier de rotation existe
        rotated_files = list(self.temp_dir.glob("test_logger.log.*"))
        self.assertGreater(len(rotated_files), 0)
    
    # Tests des utilitaires de gestion des chemins
    def test_directory_creation(self):
        """Teste la création des répertoires."""
        test_path = self.test_dir / "new_directory"
        self.path_manager.ensure_directory(test_path)  # Utilise ensure_directory au lieu de create_directory
        self.assertTrue(test_path.exists())
        self.assertTrue(test_path.is_dir())
    
    def test_config_path_preference(self):
        """Teste la préférence pour .local.conf."""
        # Crée les fichiers de configuration
        config_path = self.test_dir / "config.conf"
        local_config_path = self.test_dir / "config.local.conf"
        
        config_path.write_text("original")
        local_config_path.write_text("local")
        
        # Vérifie que .local.conf est préféré
        result = self.path_manager.get_preferred_config_path(str(config_path))  # Utilise get_preferred_config_path
        self.assertEqual(Path(result), local_config_path)
        
    def test_backup_creation(self):
        """Teste la création de backups."""
        # Crée un fichier test
        test_file = self.test_dir / "test.txt"
        test_file.write_text("test content")
        
        # Crée un backup
        backup_dir = self.test_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        backup_path = self.path_manager.backup_file(str(test_file), str(backup_dir))  # Utilise backup_file
        
        self.assertTrue(Path(backup_path).exists())
        self.assertIn("test_", Path(backup_path).name)
    
    def test_path_validation(self):
        """Teste la validation des chemins."""
        valid_path = self.test_dir / "valid"
        valid_path.mkdir()
        result, _ = self.path_manager.validate_path(valid_path)  # Utilise Path directement
        self.assertTrue(result)
        
        invalid_path = Path("/chemin/invalide")
        result, _ = self.path_manager.validate_path(invalid_path)  # Utilise Path directement
        self.assertFalse(result)
    
    def test_file_listing(self):
        """Teste le listage des fichiers."""
        # Crée quelques fichiers
        (self.test_dir / "file1.txt").write_text("")
        (self.test_dir / "file2.txt").write_text("")
        (self.test_dir / "subdir").mkdir()
        (self.test_dir / "subdir" / "file3.txt").write_text("")
        
        files = self.path_manager.list_files(str(self.test_dir), "*.txt")
        self.assertEqual(len(files), 2)  # Ne compte que les fichiers du répertoire principal
    
    # Tests de détection des caractères de contrôle
    def test_fichier_normal(self):
        """Test avec un fichier JSON normal."""
        file_path = self.binary_test_dir / "normal.json"
        file_path.write_text('{"test": "contenu normal"}', encoding='utf-8')
        
        log_path = find_control_chars_binary(str(file_path))
        self.assertIsInstance(log_path, str)  # Vérifie que le retour est une chaîne
        log_file = Path(log_path)
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("Aucun caractère de contrôle trouvé", content)
    
    def test_fichier_control(self):
        """Test avec un fichier contenant des caractères de contrôle."""
        file_path = self.binary_test_dir / "control.json"
        with open(file_path, "wb") as f:
            f.write(b'{"test": "contenu\x01avec\x02controle"}')
        
        log_path = find_control_chars_binary(str(file_path))
        self.assertIsInstance(log_path, str)  # Vérifie que le retour est une chaîne
        log_file = Path(log_path)
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("caractère de contrôle", content.lower())
    
    def test_fichier_special(self):
        """Test avec un fichier contenant des caractères spéciaux."""
        file_path = self.binary_test_dir / "special.json"
        file_path.write_text('{"test": "caractères spéciaux: éàç"}', encoding='utf-8')
        
        log_path = find_control_chars_binary(str(file_path))
        self.assertIsInstance(log_path, str)  # Vérifie que le retour est une chaîne
        log_file = Path(log_path)
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("Aucun caractère de contrôle trouvé", content)
    
    def test_fichier_vide(self):
        """Test avec un fichier vide."""
        file_path = self.binary_test_dir / "empty.json"
        file_path.touch()
        
        log_path = find_control_chars_binary(str(file_path))
        self.assertIsInstance(log_path, str)  # Vérifie que le retour est une chaîne
        log_file = Path(log_path)
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("Fichier vide", content)
    
    def test_fichier_invalide(self):
        """Test avec un fichier au format Starsector invalide."""
        file_path = self.binary_test_dir / "invalid.json"
        file_path.write_text('{"test": "retour\r\nchariot windows"}', encoding='utf-8')
        
        log_path = find_control_chars_binary(str(file_path))
        self.assertIsInstance(log_path, str)  # Vérifie que le retour est une chaîne
        log_file = Path(log_path)
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding='utf-8')
        self.assertIn("Aucun caractère de contrôle trouvé", content)
    
    def test_fichier_inexistant(self):
        """Test avec un fichier qui n'existe pas."""
        file_path = self.binary_test_dir / "inexistant.json"
        
        with self.assertRaises(FileNotFoundError):
            find_control_chars_binary(str(file_path))

if __name__ == '__main__':
    unittest.main()

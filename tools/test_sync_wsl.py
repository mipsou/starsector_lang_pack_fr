#!/usr/bin/env python3
"""
Tests unitaires pour le gestionnaire de synchronisation WSL.
"""

import unittest
import os
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
from sync_wsl import WSLSyncManager

class TestWSLSyncManager(unittest.TestCase):
    def setUp(self):
        """Création des fichiers de test temporaires."""
        self.test_dir = tempfile.mkdtemp()
        self.windows_path = Path(self.test_dir) / "windows_project"
        self.windows_path.mkdir()
        self.wsl_path = "/tmp/test_project"
        
        # Création de fichiers de test
        self._create_test_files()
        
        # Initialisation du gestionnaire
        self.sync_manager = WSLSyncManager(
            str(self.windows_path),
            self.wsl_path
        )
    
    def tearDown(self):
        """Nettoyage des fichiers de test."""
        shutil.rmtree(self.test_dir)
        # Nettoyage WSL
        subprocess.run(
            ['wsl', 'rm', '-rf', self.wsl_path],
            capture_output=True
        )
    
    def _create_test_files(self):
        """Crée des fichiers de test."""
        # Fichier de test Windows
        test_file = self.windows_path / "test.txt"
        test_file.write_text("Test content")
        
        # Sous-répertoire avec fichier
        subdir = self.windows_path / "subdir"
        subdir.mkdir()
        (subdir / "subfile.txt").write_text("Sub content")
    
    def test_path_conversion(self):
        """Test de la conversion des chemins."""
        # Windows vers WSL
        windows_path = Path("D:\\test\\path")
        wsl_path = self.sync_manager.to_wsl_path(windows_path)
        self.assertEqual(wsl_path, "/mnt/d/test/path")
        
        # WSL vers Windows
        wsl_path = "/mnt/c/test/path"
        windows_path = self.sync_manager.to_windows_path(wsl_path)
        self.assertEqual(str(windows_path), "C:\\test\\path")
    
    def test_sync_to_wsl(self):
        """Test de la synchronisation vers WSL."""
        success = self.sync_manager.sync_to_wsl()
        self.assertTrue(success)
        
        # Vérification de l'existence des fichiers dans WSL
        result = subprocess.run(
            ['wsl', 'ls', f"{self.wsl_path}/test.txt"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0)
    
    def test_sync_from_wsl(self):
        """Test de la synchronisation depuis WSL."""
        # Création d'un fichier dans WSL
        subprocess.run(
            ['wsl', 'mkdir', '-p', f"{self.wsl_path}/results"],
            capture_output=True
        )
        subprocess.run(
            ['wsl', 'bash', '-c', f"echo 'WSL content' > {self.wsl_path}/results/wsl_file.txt"],
            capture_output=True
        )
        
        success = self.sync_manager.sync_from_wsl()
        self.assertTrue(success)
        
        # Vérification du fichier Windows
        result_file = self.windows_path / "results" / "wsl_file.txt"
        self.assertTrue(result_file.exists())
    
    def test_wsl_command(self):
        """Test de l'exécution de commandes WSL."""
        success, output = self.sync_manager.run_wsl_command("echo 'test'")
        self.assertTrue(success)
        self.assertIn("test", output)

if __name__ == "__main__":
    unittest.main()

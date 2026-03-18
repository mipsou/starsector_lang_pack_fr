import unittest
import os
import shutil
import tempfile
from validate_translations import validate_mission_text, auto_correct_text, load_glossary, auto_correct_file

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests d'intégration."""
        self.test_dir = tempfile.mkdtemp()
        self.mission_dir = os.path.join(self.test_dir, "missions")
        os.makedirs(self.mission_dir)
        
        # Création d'une structure de dossiers similaire à celle du mod
        self.create_mission_structure()
        
        # Chargement du glossaire
        self.glossary = load_glossary()
    
    def create_mission_structure(self):
        """Crée une structure de dossiers de mission."""
        missions = {
            "tutorial": {
                "mission_text.txt": """Lieu : Système Corvus
Date : 3014
Objectifs : Le Space Marshal vous attend.
Description : Une Fleet ennemie approche."""
            },
            "campaign": {
                "mission1": {
                    "mission_text.txt": """Lieu : Système Corvus
Date : 3015
Objectifs : Protéger la Fleet.
Description : Test."""
                },
                "mission2": {
                    "mission_text.txt": """Lieu : Test
Date : 3016
Objectifs : Rencontrer le Space Marshal.
Description : Test."""
                }
            }
        }
        
        for mission, content in missions.items():
            if isinstance(content, dict):
                for submission, subcontent in content.items():
                    if isinstance(subcontent, dict):
                        path = os.path.join(self.mission_dir, mission, submission)
                        os.makedirs(path, exist_ok=True)
                        for filename, text in subcontent.items():
                            with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
                                f.write(text)
                    else:
                        path = os.path.join(self.mission_dir, mission)
                        os.makedirs(path, exist_ok=True)
                        with open(os.path.join(path, submission), 'w', encoding='utf-8') as f:
                            f.write(subcontent)
    
    def test_file_structure(self):
        """Test la validation sur une structure de fichiers complète."""
        errors_by_file = {}
        
        for root, dirs, files in os.walk(self.mission_dir):
            for file in files:
                if file == "mission_text.txt":
                    file_path = os.path.join(root, file)
                    errors = validate_mission_text(file_path)
                    if errors:
                        errors_by_file[file_path] = errors
        
        # Vérifie que chaque fichier a des erreurs (termes anglais)
        self.assertEqual(len(errors_by_file), 3,
                        "Devrait trouver des erreurs dans les 3 fichiers")
        
        for file_path, errors in errors_by_file.items():
            self.assertTrue(any("Space Marshal" in error or "Fleet" in error for error in errors),
                          f"Devrait trouver des termes anglais dans {file_path}")
    
    def test_file_backup(self):
        """Test la création de sauvegardes lors de la correction."""
        from validate_translations import auto_correct_file
        
        test_file = os.path.join(self.mission_dir, "tutorial", "mission_text.txt")
        original_content = None
        
        # Sauvegarde du contenu original
        with open(test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Correction du fichier
        backup_file = auto_correct_file(test_file)
        
        # Vérifie que la sauvegarde existe et contient le contenu original
        self.assertTrue(os.path.exists(backup_file),
                       "Le fichier de sauvegarde devrait exister")
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
            self.assertEqual(backup_content, original_content,
                           "La sauvegarde devrait contenir le contenu original")
        
        # Vérifie que le fichier original a été modifié
        with open(test_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
            self.assertNotEqual(new_content, original_content,
                              "Le fichier original devrait être modifié")
            self.assertIn("Maréchal Spatial", new_content,
                         "Le terme 'Space Marshal' devrait être traduit")
            self.assertIn("Flotte", new_content,
                         "Le terme 'Fleet' devrait être traduit")

    def test_concurrent_access(self):
        """Test l'accès concurrent aux fichiers."""
        import threading
        import time
        
        def validate_file(file_path, results):
            """Fonction pour valider un fichier dans un thread."""
            try:
                errors = validate_mission_text(file_path)
                results.append((file_path, errors))
            except Exception as e:
                results.append((file_path, str(e)))
        
        # Liste tous les fichiers mission_text.txt
        files_to_validate = []
        for root, dirs, files in os.walk(self.mission_dir):
            for file in files:
                if file == "mission_text.txt":
                    files_to_validate.append(os.path.join(root, file))
        
        # Crée et démarre les threads
        results = []
        threads = []
        for file_path in files_to_validate:
            thread = threading.Thread(target=validate_file,
                                   args=(file_path, results))
            threads.append(thread)
            thread.start()
        
        # Attend que tous les threads soient terminés
        for thread in threads:
            thread.join()
        
        # Vérifie les résultats
        self.assertEqual(len(results), len(files_to_validate),
                        "Tous les fichiers devraient être validés")
        
        for file_path, result in results:
            self.assertIsInstance(result, list,
                                f"La validation de {file_path} devrait retourner une liste d'erreurs")
    
    def test_error_handling(self):
        """Test la gestion des erreurs."""
        # Test avec un fichier inexistant
        with self.assertRaises(FileNotFoundError):
            validate_mission_text("fichier_inexistant.txt")
        
        # Test avec un fichier vide
        empty_file = os.path.join(self.test_dir, "empty.txt")
        with open(empty_file, 'w', encoding='utf-8') as f:
            pass
        
        errors = validate_mission_text(empty_file)
        self.assertTrue(errors, "Un fichier vide devrait générer des erreurs")
        
        # Test avec un fichier non UTF-8
        binary_file = os.path.join(self.test_dir, "binary.txt")
        with open(binary_file, 'wb') as f:
            f.write(b'\x80\x81')
        
        with self.assertRaises(UnicodeDecodeError):
            validate_mission_text(binary_file)
    
    def tearDown(self):
        """Nettoyage après les tests."""
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)

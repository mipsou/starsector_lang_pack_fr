import unittest
import os
import tempfile
from validate_translations import (
    validate_mission_text,
    auto_correct_text,
    load_glossary
)

class TestValidateTranslations(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests."""
        self.test_dir = tempfile.mkdtemp()
        
        # Création d'un glossaire de test
        self.glossary_content = """en,fr
Space Marshal,Maréchal Spatial
Corvus System,Système Corvus
Fleet,Flotte"""
        self.glossary_path = os.path.join(self.test_dir, "glossary.csv")
        with open(self.glossary_path, "w", encoding="utf-8") as f:
            f.write(self.glossary_content)
    
    def create_test_file(self, content):
        """Crée un fichier de test avec le contenu spécifié."""
        file_path = os.path.join(self.test_dir, "mission_text.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path
    
    def test_structure_validation(self):
        """Test de la validation de la structure."""
        # Test avec une structure valide
        content = """Lieu : Test
Date : 3014
Objectifs : Test
Description : Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertEqual(len(errors), 0, "Le fichier valide ne devrait pas avoir d'erreurs")
        
        # Test avec une structure invalide
        content = """Test invalide
Sans structure"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Lieu :" in error for error in errors), 
                       "Devrait détecter l'absence de 'Lieu :'")
    
    def test_typography_validation(self):
        """Test de la validation typographique."""
        # Test des espaces avant/après la ponctuation
        content = """Lieu:Test
Date:3014
Objectifs:Test!Description:Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Espace manquante" in error for error in errors),
                       "Devrait détecter les espaces manquantes")
    
    def test_glossary_validation(self):
        """Test de la validation du glossaire."""
        content = """Lieu : Test
Date : 3014
Objectifs : Le Space Marshal dirige la Fleet
Description : Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Space Marshal" in error for error in errors),
                       "Devrait détecter le terme anglais 'Space Marshal'")
        self.assertTrue(any("Fleet" in error for error in errors),
                       "Devrait détecter le terme anglais 'Fleet'")
    
    def test_auto_correction(self):
        """Test de la correction automatique."""
        content = """Lieu:Test
Date:3014
Objectifs:Le Space Marshal dirige la Fleet!
Description:Test"""
        
        glossary = load_glossary()
        corrected = auto_correct_text(content, glossary)
        
        # Vérifie la correction des espaces
        self.assertIn("Lieu : ", corrected,
                     "Devrait corriger les espaces avant/après les deux-points")
        
        # Vérifie la correction des termes anglais
        self.assertIn("Maréchal Spatial", corrected,
                     "Devrait remplacer 'Space Marshal' par 'Maréchal Spatial'")
        self.assertIn("Flotte", corrected,
                     "Devrait remplacer 'Fleet' par 'Flotte'")
    
    def test_empty_file(self):
        """Test avec un fichier vide."""
        file_path = self.create_test_file("")
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Lieu :" in error for error in errors),
                       "Devrait détecter un fichier vide")
    
    def test_missing_sections(self):
        """Test avec des sections manquantes."""
        content = """Lieu : Test
Description : Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Date :" in error for error in errors),
                       "Devrait détecter l'absence de la section Date")
        self.assertTrue(any("Objectifs :" in error for error in errors),
                       "Devrait détecter l'absence de la section Objectifs")
    
    def test_special_characters(self):
        """Test avec des caractères spéciaux."""
        content = """Lieu : Test...
Date : 3014
Objectifs : Test "citation" test
Description : Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("points de suspension" in error for error in errors),
                       "Devrait détecter les points de suspension incorrects")
        self.assertTrue(any("guillemets français" in error for error in errors),
                       "Devrait détecter les guillemets droits")
    
    def test_case_sensitivity(self):
        """Test de la sensibilité à la casse."""
        content = """Lieu : Test
Date : 3014
Objectifs : Le SPACE MARSHAL et la space fleet
Description : Test"""
        file_path = self.create_test_file(content)
        errors = validate_mission_text(file_path)
        self.assertTrue(any("Space Marshal" in error for error in errors),
                       "Devrait détecter le terme anglais indépendamment de la casse")
        self.assertTrue(any("Fleet" in error for error in errors),
                       "Devrait détecter le terme anglais indépendamment de la casse")
        
        # Test de la correction automatique
        glossary = load_glossary()
        corrected = auto_correct_text(content, glossary)
        self.assertIn("Maréchal Spatial", corrected,
                     "Devrait corriger le terme anglais en majuscules")
        self.assertIn("Flotte", corrected,
                     "Devrait corriger le terme anglais en minuscules")

    def tearDown(self):
        """Nettoyage après les tests."""
        # Supprime les fichiers de test
        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()

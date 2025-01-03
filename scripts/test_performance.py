import unittest
import tempfile
import os
import time
import random
import string
from validate_translations import validate_mission_text, auto_correct_text, load_glossary

class TestPerformance(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests de performance."""
        self.test_dir = tempfile.mkdtemp()
        self.sample_texts = self._generate_sample_texts()
        self.glossary = load_glossary()
    
    def _generate_sample_texts(self):
        """Génère des textes de test de différentes tailles."""
        texts = []
        sizes = [1, 10, 100, 1000]  # Tailles en KB
        
        for size in sizes:
            text = f"Lieu : Test\nDate : 3014\nObjectifs : "
            # Ajoute du texte aléatoire avec quelques termes du glossaire
            words = ['Space Marshal', 'Fleet', 'test', 'mission'] * (size * 25)
            random.shuffle(words)
            text += ' '.join(words)
            texts.append((size, text))
        
        return texts
    
    def _create_test_files(self, num_files):
        """Crée un nombre spécifié de fichiers de test."""
        files = []
        for i in range(num_files):
            size, content = random.choice(self.sample_texts)
            file_path = os.path.join(self.test_dir, f"mission_{i}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files.append((size, file_path))
        return files
    
    def test_validation_performance(self):
        """Test les performances de la validation."""
        print("\nTest de performance de la validation :")
        
        # Test avec différentes tailles de fichiers
        for size, text in self.sample_texts:
            file_path = os.path.join(self.test_dir, f"test_{size}kb.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            start_time = time.time()
            errors = validate_mission_text(file_path)
            duration = time.time() - start_time
            
            print(f"- Fichier de {size}KB : {duration:.3f} secondes")
            self.assertLess(duration, size * 0.1,
                          f"La validation d'un fichier de {size}KB ne devrait pas prendre plus de {size * 0.1} secondes")
    
    def test_correction_performance(self):
        """Test les performances de la correction automatique."""
        print("\nTest de performance de la correction :")
        
        for size, text in self.sample_texts:
            start_time = time.time()
            corrected = auto_correct_text(text, self.glossary)
            duration = time.time() - start_time
            
            print(f"- Texte de {size}KB : {duration:.3f} secondes")
            self.assertLess(duration, size * 0.1,
                          f"La correction d'un texte de {size}KB ne devrait pas prendre plus de {size * 0.1} secondes")
    
    def test_multiple_files(self):
        """Test avec plusieurs fichiers."""
        print("\nTest avec plusieurs fichiers :")
        
        num_files = [10, 100]
        for count in num_files:
            files = self._create_test_files(count)
            
            start_time = time.time()
            for _, file_path in files:
                validate_mission_text(file_path)
            duration = time.time() - start_time
            
            print(f"- {count} fichiers : {duration:.3f} secondes")
            self.assertLess(duration, count * 0.1,
                          f"La validation de {count} fichiers ne devrait pas prendre plus de {count * 0.1} secondes")
    
    def test_memory_usage(self):
        """Test de la consommation mémoire."""
        import psutil
        import os
        
        print("\nTest de la consommation mémoire :")
        process = psutil.Process()
        
        # Test avec le plus grand fichier
        size, text = self.sample_texts[-1]
        file_path = os.path.join(self.test_dir, "large_file.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # En MB
        validate_mission_text(file_path)
        final_memory = process.memory_info().rss / 1024 / 1024
        
        memory_used = final_memory - initial_memory
        print(f"- Mémoire utilisée : {memory_used:.2f} MB")
        self.assertLess(memory_used, 100,
                       "La validation ne devrait pas utiliser plus de 100MB de mémoire")
    
    def tearDown(self):
        """Nettoyage après les tests."""
        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)

"""
Tests unitaires pour le module fix_quotes.

Ce module teste la fonction convert_quotes_starsector du module fix_quotes
pour s'assurer qu'elle respecte les règles de conversion des guillemets
selon la typographie française et le format JSON de Starsector.
"""

import unittest
from fix_quotes import convert_quotes_starsector

class TestQuotesStarsector(unittest.TestCase):
    """Test de la conversion des guillemets pour Starsector."""
    
    def setUp(self):
        """Initialisation des constantes pour les tests."""
        self.ESPACE_FINE = '\u202F'
    
    def test_simple_conversion(self):
        """Test de conversion simple."""
        self.assertEqual(
            convert_quotes_starsector('"Test"'),
            '"Test"'  # Les guillemets externes sont préservés
        )
    
    def test_structure_json(self):
        """Test de préservation de la structure JSON."""
        self.assertEqual(
            convert_quotes_starsector('{"key":"value"}'),
            '{"key":"value"}'  # Les guillemets de structure sont préservés
        )
    
    def test_format_tips(self):
        """Test du format spécifique tips.json."""
        self.assertEqual(
            convert_quotes_starsector('{tips:[{freq:1,tip:"Test"}]}'),
            '{tips:[{freq:1,tip:"Test"}]}'  # Structure préservée
        )
    
    def test_guillemets_imbriques(self):
        """Test des guillemets imbriqués."""
        self.assertEqual(
            convert_quotes_starsector('"texte avec "citation" interne"'),
            f'"texte avec «{self.ESPACE_FINE}citation{self.ESPACE_FINE}» interne"'
        )
    
    def test_guillemets_echappes(self):
        """Test des guillemets échappés."""
        self.assertEqual(
            convert_quotes_starsector(r'"texte avec \"guillemets\" échappés"'),
            f'"texte avec «{self.ESPACE_FINE}guillemets{self.ESPACE_FINE}» échappés"'
        )
    
    def test_preservation_structure(self):
        """Test de préservation des structures spéciales."""
        self.assertEqual(
            convert_quotes_starsector('tips:["Test"]'),
            'tips:["Test"]'  # Structure préservée
        )
    
    def test_double_imbrication(self):
        """Test des guillemets doublement imbriqués."""
        self.assertEqual(
            convert_quotes_starsector('"texte avec "citation contenant une "autre citation" imbriquée" et la suite"'),
            f'"texte avec «{self.ESPACE_FINE}citation contenant une ‹{self.ESPACE_FINE}autre citation{self.ESPACE_FINE}› imbriquée{self.ESPACE_FINE}» et la suite"'
        )
    
    def test_ponctuation(self):
        """Test de la ponctuation avec les guillemets."""
        # La virgule et le point doivent être à l'intérieur des guillemets
        self.assertEqual(
            convert_quotes_starsector('"texte avec "une citation, avec ponctuation." et la suite"'),
            f'"texte avec «{self.ESPACE_FINE}une citation, avec ponctuation.{self.ESPACE_FINE}» et la suite"'
        )
        # Le point d'interrogation peut être à l'extérieur selon le contexte
        self.assertEqual(
            convert_quotes_starsector('"texte avec "une question ?" important"'),
            f'"texte avec «{self.ESPACE_FINE}une question{self.ESPACE_FINE}» ? important"'
        )

if __name__ == '__main__':
    unittest.main()

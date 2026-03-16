#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
import re
from pathlib import Path

def read_starsector_json(file_path):
    """Lit un fichier JSON au format Starsector."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nettoyer le contenu et remplacer les retours à la ligne par des espaces
    content = ' '.join(line.strip() for line in content.split('\n'))
    
    # Extraire les tips
    tips_match = re.search(r'tips:\[(.*?)\]', content, re.DOTALL)
    if not tips_match:
        pytest.fail(f"Format invalide dans {file_path}")
    
    tips_content = tips_match.group(1).strip()
    
    # Construire un JSON valide avec juste le tableau
    json_content = f"[{tips_content}]"
    
    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        pytest.fail(f"Erreur de lecture du fichier {file_path}: {str(e)}")

class TestTips:
    """Tests pour la validation des tips."""
    
    @pytest.fixture
    def tips_file(self):
        """Fixture pour le fichier de tips."""
        return Path('localization/fr/data/strings/tips.json')
    
    @pytest.fixture
    def original_tips(self):
        """Fixture pour les tips originaux."""
        return Path('original/data/strings/tips.json')
    
    def test_tips_file_exists(self, tips_file):
        """Vérifie que le fichier de tips existe."""
        assert tips_file.exists(), f"Le fichier {tips_file} n'existe pas"
    
    def test_tips_is_valid_json(self, tips_file):
        """Vérifie que le fichier est un JSON valide."""
        try:
            read_starsector_json(tips_file)
        except Exception as e:
            pytest.fail(f"Le fichier {tips_file} n'est pas un JSON valide: {str(e)}")

    def test_tips_structure_matches_original(self, tips_file, original_tips):
        """Vérifie que la structure correspond à l'original."""
        try:
            translated = read_starsector_json(tips_file)
            original = read_starsector_json(original_tips)
            assert len(translated) == len(original), \
                f"Nombre de tips différent: {len(translated)} vs {len(original)}"
            
            for i, (trans, orig) in enumerate(zip(translated, original)):
                if isinstance(orig, dict):
                    assert isinstance(trans, dict), \
                        f"Le tip {i} devrait être un objet"
                    assert "freq" in trans and "tip" in trans, \
                        f"Le tip {i} n'a pas les champs requis"
                    assert trans["freq"] == orig["freq"], \
                        f"Fréquence différente pour le tip {i}"
                else:
                    assert isinstance(trans, str), \
                        f"Le tip {i} devrait être une chaîne"
        except Exception as e:
            pytest.fail(f"Erreur lors de la comparaison: {str(e)}")

    def test_tips_no_empty_translations(self, tips_file):
        """Vérifie qu'il n'y a pas de traductions vides."""
        tips = read_starsector_json(tips_file)
        for i, tip in enumerate(tips):
            if isinstance(tip, dict):
                assert tip["tip"].strip(), f"Traduction vide pour le tip {i}"
            else:
                assert tip.strip(), f"Traduction vide pour le tip {i}"

    def test_tips_french_typography(self, tips_file):
        """Vérifie la typographie française."""
        tips = read_starsector_json(tips_file)
        
        for i, tip in enumerate(tips):
            text = tip["tip"] if isinstance(tip, dict) else tip
            
            # Vérifie les guillemets
            assert "«" not in text and "»" not in text, \
                f"Guillemets français trouvés dans le tip {i}"
            
            # Vérifie les apostrophes
            assert "'" not in text, \
                f"Apostrophe française trouvée dans le tip {i}"
            
            # Vérifie les espaces avant la ponctuation
            assert not re.search(r'\s+[.,;:!?]', text), \
                f"Espace avant la ponctuation dans le tip {i}"

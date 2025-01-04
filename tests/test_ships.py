#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from pathlib import Path
import re

class TestShips:
    """Tests pour la validation des descriptions de vaisseaux."""
    
    @pytest.fixture
    def ships_file(self):
        """Fixture pour le fichier des vaisseaux."""
        return Path('localization/fr/data/hulls/ship_data.json')
    
    @pytest.fixture
    def original_ships_file(self):
        """Fixture pour le fichier original des vaisseaux."""
        return Path('original/data/hulls/ship_data.json')
    
    def test_ships_file_exists(self, ships_file):
        """Vérifie que le fichier des vaisseaux existe."""
        assert ships_file.exists(), f"Le fichier {ships_file} n'existe pas"
    
    def test_ships_valid_json(self, ships_file):
        """Vérifie que le fichier est un JSON valide."""
        try:
            with open(ships_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Le fichier {ships_file} n'est pas un JSON valide: {str(e)}")
    
    def test_ships_structure(self, ships_file, original_ships_file):
        """Vérifie la structure des données des vaisseaux."""
        with open(ships_file, 'r', encoding='utf-8') as f:
            translated = json.load(f)
        with open(original_ships_file, 'r', encoding='utf-8') as f:
            original = json.load(f)
            
        # Vérifie que tous les vaisseaux sont présents
        missing_ships = set(original.keys()) - set(translated.keys())
        assert not missing_ships, f"Vaisseaux manquants: {missing_ships}"
        
        # Vérifie la structure pour chaque vaisseau
        structure_errors = []
        for ship_id, ship_data in translated.items():
            if ship_id not in original:
                continue
                
            orig_ship = original[ship_id]
            # Vérifie les champs requis
            required_fields = {'name', 'description', 'designation'}
            for field in required_fields:
                if field not in ship_data and field in orig_ship:
                    structure_errors.append(
                        (ship_id, f"Champ manquant: {field}")
                    )
                    
        assert not structure_errors, f"Erreurs de structure: {structure_errors}"
    
    def test_ships_no_empty_translations(self, ships_file):
        """Vérifie qu'il n'y a pas de traductions vides."""
        with open(ships_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        empty_translations = []
        for ship_id, ship_data in data.items():
            for field in ['name', 'description', 'designation']:
                if field in ship_data and not ship_data[field].strip():
                    empty_translations.append((ship_id, field))
                    
        assert not empty_translations, \
            f"Traductions vides trouvées: {empty_translations}"
    
    def test_ships_terminology(self, ships_file):
        """Vérifie la cohérence terminologique."""
        with open(ships_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        terminology_errors = []
        
        # Termes à vérifier (à compléter selon les besoins)
        terms = {
            'fighter': 'chasseur',
            'frigate': 'frégate',
            'destroyer': 'destroyer',
            'cruiser': 'croiseur',
            'capital ship': 'vaisseau capital'
        }
        
        for ship_id, ship_data in data.items():
            description = ship_data.get('description', '').lower()
            for en_term, fr_term in terms.items():
                if en_term in description and fr_term not in description:
                    terminology_errors.append(
                        (ship_id, f"Terme '{en_term}' non traduit par '{fr_term}'")
                    )
                    
        assert not terminology_errors, \
            f"Erreurs de terminologie: {terminology_errors}"
    
    def test_ships_french_format(self, ships_file):
        """Vérifie le format français des descriptions."""
        with open(ships_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        format_errors = []
        
        for ship_id, ship_data in data.items():
            description = ship_data.get('description', '')
            
            # Vérifie les espaces avant la ponctuation double
            if re.search(r'[;:!?](?!\s)', description):
                format_errors.append(
                    (ship_id, "Espace manquant avant ponctuation double")
                )
                
            # Vérifie les guillemets français
            if '"' in description:
                format_errors.append(
                    (ship_id, "Guillemets droits au lieu de guillemets français")
                )
                
        assert not format_errors, f"Erreurs de format: {format_errors}"

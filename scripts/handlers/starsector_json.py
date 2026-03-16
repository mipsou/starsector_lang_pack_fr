#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parser JSON spécifique au format Starsector avec analyse des structures originales.
"""

import logging
import os
import re
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import json

class FileType(Enum):
    """Types de fichiers supportés."""
    STRINGS = auto()
    TIPS = auto()
    TOOLTIPS = auto()
    DESCRIPTIONS = auto()  # Format spécial : tableau de traductions
    UNKNOWN = auto()

class StructureMap:
    """Carte des structures JSON originales."""
    def __init__(self):
        self.variables: Set[str] = set()  # Variables système ($faction, etc.)
        self.sections: Dict[str, Set[str]] = {}  # Sections et leurs clés
        self.patterns: Dict[str, str] = {}  # Motifs de structure
        self.required_fields: Set[str] = set()  # Champs obligatoires

    def add_variable(self, var: str):
        """Ajoute une variable système."""
        self.variables.add(var)

    def add_section(self, section: str, keys: Set[str]):
        """Ajoute une section et ses clés."""
        self.sections[section] = keys

    def add_pattern(self, key: str, pattern: str):
        """Ajoute un motif de structure."""
        self.patterns[key] = pattern

    def add_required_field(self, field: str):
        """Ajoute un champ obligatoire."""
        self.required_fields.add(field)

class StarsectorJsonAnalyzer:
    """Analyseur de fichiers JSON Starsector."""
    
    def __init__(self, starsector_root: str):
        self.root = Path(starsector_root)
        self.structure_maps: Dict[FileType, StructureMap] = {}
        self._analyze_original_files()

    def _analyze_original_files(self):
        """Analyse les fichiers originaux pour créer les cartes de structure."""
        # Analyse strings.json
        strings_path = self.root / "starsector-core/data/strings/strings.json"
        if strings_path.exists():
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            data, _ = parse_starsector_json(content)
            if data:
                self._create_strings_map(data)

        # Analyse tips.json
        tips_path = self.root / "starsector-core/data/strings/tips.json"
        if tips_path.exists():
            with open(tips_path, 'r', encoding='utf-8') as f:
                content = f.read()
            data, _ = parse_starsector_json(content)
            if data:
                self._create_tips_map(data)

        # Analyse tooltips.json
        tooltips_path = self.root / "starsector-core/data/strings/tooltips.json"
        if tooltips_path.exists():
            with open(tooltips_path, 'r', encoding='utf-8') as f:
                content = f.read()
            data, _ = parse_starsector_json(content)
            if data:
                self._create_tooltips_map(data)

        # Analyse descriptions.json
        descriptions_path = self.root / "starsector-core/data/strings/descriptions.json"
        if descriptions_path.exists():
            with open(descriptions_path, 'r', encoding='utf-8') as f:
                content = f.read()
            data, _ = parse_starsector_json(content)
            if data:
                self._create_descriptions_map(data)

    def _create_strings_map(self, data: Dict):
        """Crée la carte de structure pour strings.json."""
        structure = StructureMap()
        
        def extract_variables(text: str):
            """Extrait les variables système d'un texte."""
            vars = re.findall(r'\$\w+', text)
            for var in vars:
                structure.add_variable(var)

        # Analyse la structure
        for key, value in data.items():
            if isinstance(value, dict):
                subsection_keys = set()
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, str):
                        extract_variables(subvalue)
                    subsection_keys.add(subkey)
                structure.add_section(key, subsection_keys)
            elif isinstance(value, str):
                extract_variables(value)

        self.structure_maps[FileType.STRINGS] = structure

    def _create_tips_map(self, data: List):
        """Crée la carte de structure pour tips.json."""
        structure = StructureMap()
        
        # Analyse la structure des objets tips
        for item in data:
            if isinstance(item, dict):
                for key in item.keys():
                    structure.add_required_field(key)

        self.structure_maps[FileType.TIPS] = structure

    def _create_tooltips_map(self, data: Dict):
        """Crée la carte de structure pour tooltips.json."""
        structure = StructureMap()
        
        # Analyse la structure
        for section, content in data.items():
            if isinstance(content, dict):
                keys = set(content.keys())
                structure.add_section(section, keys)
                if 'title' in keys:
                    structure.add_required_field('title')
                if 'body' in keys:
                    structure.add_required_field('body')

        self.structure_maps[FileType.TOOLTIPS] = structure

    def _create_descriptions_map(self, data: List):
        """Crée la carte de structure pour descriptions.json."""
        structure = StructureMap()
        
        # Analyse la structure
        for item in data:
            if isinstance(item, dict):
                keys = set(item.keys())
                if 'key' in keys and 'original' in keys and 'translation' in keys and 'stage' in keys:
                    structure.add_required_field('key')
                    structure.add_required_field('original')
                    structure.add_required_field('translation')
                    structure.add_required_field('stage')

        self.structure_maps[FileType.DESCRIPTIONS] = structure

    def validate_structure(self, data: Any, file_type: FileType) -> Tuple[bool, Optional[str]]:
        """Valide la structure d'un fichier selon sa carte."""
        if file_type not in self.structure_maps:
            return True, None  # Pas de carte = pas de validation

        structure = self.structure_maps[file_type]

        if file_type == FileType.STRINGS:
            # Vérifie les sections et variables
            for key, value in data.items():
                if isinstance(value, dict):
                    if key in structure.sections:
                        expected_keys = structure.sections[key]
                        for subkey in value.keys():
                            if subkey not in expected_keys:
                                return False, f"Clé inattendue dans la section {key}: {subkey}"
                    else:
                        return False, f"Section inconnue: {key}"

        elif file_type == FileType.TIPS:
            # Vérifie les champs requis dans les objets
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        for field in structure.required_fields:
                            if field not in item:
                                return False, f"Champ requis manquant: {field}"

        elif file_type == FileType.TOOLTIPS:
            # Vérifie les sections et champs requis
            for section, content in data.items():
                if isinstance(content, dict):
                    if section in structure.sections:
                        expected_keys = structure.sections[section]
                        for key in content.keys():
                            if key not in expected_keys:
                                return False, f"Clé inattendue dans {section}: {key}"
                    for field in structure.required_fields:
                        if field not in content:
                            return False, f"Champ requis manquant dans {section}: {field}"

        elif file_type == FileType.DESCRIPTIONS:
            # Vérifie les champs requis
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        for field in structure.required_fields:
                            if field not in item:
                                return False, f"Champ requis manquant: {field}"

        return True, None

# Fonctions existantes mises à jour pour utiliser l'analyseur
analyzer = None

def init_analyzer(starsector_root: str):
    """Initialise l'analyseur avec le répertoire racine de Starsector."""
    global analyzer
    analyzer = StarsectorJsonAnalyzer(starsector_root)

def detect_file_type(data: Any) -> FileType:
    """
    Détecte le type de fichier à partir de son contenu.
    
    Args:
        data: Données JSON parsées
        
    Returns:
        Type du fichier détecté
    """
    try:
        # Vérifie le format strings.json (clé strings avec text)
        if isinstance(data, dict) and "strings" in data:
            if isinstance(data["strings"], dict):
                for item in data["strings"].values():
                    if isinstance(item, dict) and "text" in item:
                        return FileType.STRINGS
                return FileType.STRINGS  # Même si vide, c'est un fichier strings

        # Vérifie le format tips.json (tableau de tips)
        if isinstance(data, dict) and "tips" in data:
            if isinstance(data["tips"], list):
                return FileType.TIPS

        # Vérifie le format tooltips.json (sections avec title/body)
        if isinstance(data, dict):
            for section, content in data.items():
                if isinstance(content, dict):
                    for item in content.values():
                        if isinstance(item, dict) and "title" in item and "body" in item:
                            return FileType.TOOLTIPS
                    break

        # Vérifie le format descriptions.json (tableau avec key/original/translation)
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                required_fields = {"key", "original", "translation", "stage"}
                if all(field in first_item for field in required_fields):
                    return FileType.DESCRIPTIONS
        
        return FileType.UNKNOWN
        
    except Exception as e:
        logging.error(f"Erreur lors de la détection du type de fichier : {str(e)}")
        return FileType.UNKNOWN

def format_starsector_json(content: dict) -> str:
    """
    Formate un dictionnaire en JSON selon les conventions Starsector.
    
    Args:
        content: Dictionnaire à formater
        
    Returns:
        str: Chaîne JSON formatée
    """
    try:
        # Convertit en JSON avec indentation
        json_str = json.dumps(content, ensure_ascii=False, indent=4)
        # Ajoute les virgules finales requises par le format Starsector
        json_str = re.sub(r'([}\]])(,?\s*[}\]])', r'\1,\2', json_str)
        return json_str
    except Exception as e:
        logging.error(f"Erreur lors du formatage JSON : {str(e)}")
        return ""

def parse_starsector_json(text: str) -> dict:
    """
    Parse une chaîne JSON au format Starsector.
    
    Args:
        text: Texte JSON à parser
        
    Returns:
        dict: Dictionnaire parsé
    """
    try:
        # Supprime les virgules finales superflues
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        return json.loads(text)
    except Exception as e:
        logging.error(f"Erreur lors du parsing JSON : {str(e)}")
        return {}

logger = logging.getLogger(__name__)

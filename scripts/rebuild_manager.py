#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestionnaire global de reconstruction de fichiers.
"""

import logging
import shutil
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from handlers.json.models import ValidationResult
from handlers.json.validator import JsonValidator, FileType as JsonFileType
from handlers.json.writer import JsonWriter
from handlers.json.handler import JsonHandler
from handlers.starsector_json import parse_starsector_json

# Initialisation du logger
logger = logging.getLogger(__name__)

# Initialisation du handler JSON
json_handler = JsonHandler(logger)

class FileType(Enum):
    """Types de fichiers supportés."""
    JSON = auto()
    CSV = auto()
    INI = auto()
    CUSTOM = auto()

    @classmethod
    def from_extension(cls, ext: str) -> Optional['FileType']:
        """Retourne le type de fichier correspondant à l'extension."""
        ext = ext.lower()
        if ext == '.json':
            return cls.JSON
        elif ext == '.csv':
            return cls.CSV
        elif ext == '.ini':
            return cls.INI
        return None

class FormatSpec:
    """Spécification du format d'un type de fichier."""
    def __init__(self):
        self.indent_char: str = "\t"  # Caractère d'indentation
        self.indent_size: int = 1     # Nombre de caractères d'indentation
        self.newline: str = "\n"      # Type de saut de ligne
        self.encoding: str = "utf-8"  # Encodage du fichier
        self.patterns: Dict[str, str] = {}  # Motifs de structure à préserver
        self.required_fields: List[str] = []  # Champs obligatoires
        self.comment_char: str = "#"  # Caractère de commentaire
        self.custom_rules: Dict[str, Any] = {}  # Règles spécifiques au format

class RebuildManager:
    """Gestionnaire de reconstruction de fichiers."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.format_specs: Dict[str, FormatSpec] = {}
        self.backup_path: Optional[Path] = None
        self.verbose = False
    
    def set_verbose(self, verbose: bool):
        """Active ou désactive le mode verbeux."""
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
    
    def set_backup_path(self, path: Path):
        """Définit le chemin des sauvegardes."""
        self.backup_path = path
    
    def register_format(self, file_pattern: str, spec: FormatSpec):
        """Enregistre une spécification de format pour un type de fichier."""
        self.format_specs[file_pattern] = spec
        if self.verbose:
            logging.debug(f"Format enregistré pour {file_pattern}")
    
    def get_format_spec(self, file_path: Path) -> Optional[FormatSpec]:
        """Récupère la spécification de format pour un fichier."""
        for pattern, spec in self.format_specs.items():
            if file_path.match(pattern):
                return spec
        return None
    
    def analyze_original(self, file_path: Path) -> FormatSpec:
        """Analyse le fichier original pour détecter son format."""
        spec = FormatSpec()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Détecte l'indentation
            lines = content.split('\n')
            for line in lines:
                if line.startswith('\t'):
                    spec.indent_char = '\t'
                    spec.indent_size = 1
                    break
                elif line.startswith('    '):
                    spec.indent_char = ' '
                    spec.indent_size = 4
                    break
            
            # Détecte les patterns spécifiques à Starsector
            if '"tips":[' in content:
                spec.patterns['tips'] = '['
            if '"freq":' in content:
                spec.patterns['freq'] = '0'
            
            # Détecte l'encodage
            spec.encoding = 'utf-8'
            
            return spec
            
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse du format : {str(e)}")
            return spec
    
    def rebuild_file(self, original_path: Path, output_path: Path) -> bool:
        """Reconstruit un fichier en préservant les traductions existantes."""
        try:
            # Vérifie que le fichier original existe
            if not original_path.exists():
                logging.error(f"Fichier original non trouvé : {original_path}")
                return False
            
            # Analyse le format du fichier original
            spec = self.get_format_spec(original_path)
            if not spec:
                spec = self.analyze_original(original_path)
            
            # Lit le contenu du fichier original
            with open(original_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Détermine le type de fichier
            file_type = FileType.from_extension(original_path.suffix)
            
            # Crée le dossier de sortie si nécessaire
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Reconstruit selon le type
            if file_type == FileType.JSON:
                return self._rebuild_json(content, None, output_path, spec)
            elif file_type == FileType.CSV:
                return self._rebuild_csv(content, None, output_path, spec)
            elif file_type == FileType.INI:
                return self._rebuild_ini(content, None, output_path, spec)
            else:
                logging.error(f"Type de fichier non supporté : {original_path.suffix}")
                return False
                
        except Exception as e:
            logging.error(f"Erreur lors de la reconstruction : {str(e)}")
            return False
            
    def _rebuild_json(self, content: str, existing_data: Optional[Dict], 
                    output_path: Path, spec: FormatSpec) -> bool:
        """Reconstruit un fichier JSON en préservant le format exact de Starsector."""
        try:
            # Parse le contenu JSON
            data = json_handler.parse(content)
            
            # Écrit le fichier en préservant le format exact
            with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
                # Utilise un encoder personnalisé pour le format Starsector
                class StarsectorEncoder(json_handler.JsonEncoder):
                    def __init__(self, **kwargs):
                        super().__init__(**kwargs)
                        self.indent_char = '\t'  # Toujours utiliser des tabulations
                        self.indent_size = 1
                        self.current_indent = 0
                    
                    def encode(self, obj):
                        if isinstance(obj, (dict, list)):
                            lines = []
                            if isinstance(obj, dict):
                                self.current_indent += 1
                                for key, value in obj.items():
                                    indent = self.indent_char * self.current_indent
                                    if isinstance(value, (dict, list)):
                                        lines.append(f'{indent}"{key}":{self.encode(value)}')
                                    elif isinstance(value, (int, float)):
                                        lines.append(f'{indent}"{key}":{value}')
                                    else:
                                        lines.append(f'{indent}"{key}":"{value}"')
                                self.current_indent -= 1
                                return "{\n" + ",\n".join(lines) + "\n" + (self.indent_char * self.current_indent) + "}"
                            else:  # list
                                self.current_indent += 1
                                items = []
                                for item in obj:
                                    indent = self.indent_char * self.current_indent
                                    if isinstance(item, (dict, list)):
                                        items.append(f"{indent}{self.encode(item)}")
                                    elif isinstance(item, (int, float)):
                                        items.append(f"{indent}{item}")
                                    else:
                                        items.append(f'{indent}"{item}"')
                                self.current_indent -= 1
                                return "[\n" + ",\n".join(items) + "\n" + (self.indent_char * self.current_indent) + "]"
                        elif isinstance(obj, (int, float)):
                            return str(obj)
                        return f'"{obj}"'  # Guillemets droits pour les chaînes
                
                # Écrit avec l'encoder Starsector
                json_str = StarsectorEncoder().encode(data)
                f.write(json_str)
            
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de la reconstruction JSON : {str(e)}")
            return False
    
    def _rebuild_csv(self, content: str, existing_data: Optional[Dict], 
                    output_path: Path, spec: FormatSpec) -> bool:
        """Reconstruit un fichier CSV en préservant son format exact."""
        try:
            import csv
            from io import StringIO
            
            # Parse le CSV original
            reader = csv.reader(StringIO(content), dialect=csv.excel)
            headers = next(reader)  # Première ligne = en-têtes
            rows = list(reader)
            
            # Écrit le fichier
            with open(output_path, 'w', encoding=spec.encoding, newline='') as f:
                writer = csv.writer(f, dialect=csv.excel)
                writer.writerow(headers)
                writer.writerows(rows)
            
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de la reconstruction CSV : {str(e)}")
            return False
    
    def _rebuild_ini(self, content: str, existing_data: Optional[Dict], 
                    output_path: Path, spec: FormatSpec) -> bool:
        """Reconstruit un fichier INI en préservant son format exact."""
        try:
            import configparser
            from io import StringIO
            
            # Parse le fichier INI original
            config = configparser.ConfigParser()
            config.optionxform = str  # Préserve la casse des clés
            config.read_string(content)
            
            # Écrit le fichier en préservant le format
            with open(output_path, 'w', encoding=spec.encoding) as f:
                config.write(f, space_around_delimiters=False)  # Format compact
            
            # Corrige le format si nécessaire
            if spec.indent_char or spec.comment_char != '#':
                with open(output_path, 'r', encoding=spec.encoding) as f:
                    lines = f.readlines()
                
                # Applique l'indentation et le format des commentaires
                formatted_lines = []
                for line in lines:
                    if line.startswith('['):
                        formatted_lines.append(line)  # Sections sans indentation
                    elif line.startswith('#'):
                        # Remplace le caractère de commentaire si différent
                        if spec.comment_char != '#':
                            line = spec.comment_char + line[1:]
                        formatted_lines.append(line)
                    elif '=' in line:
                        # Ajoute l'indentation aux clés/valeurs
                        formatted_lines.append(spec.indent_char * spec.indent_size + line)
                    else:
                        formatted_lines.append(line)
                
                # Réécrit le fichier avec le bon format
                with open(output_path, 'w', encoding=spec.encoding) as f:
                    f.writelines(formatted_lines)
            
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de la reconstruction INI : {str(e)}")
            return False

    def rebuild_json_file(self, file_path: Path) -> ValidationResult:
        """Reconstruit un fichier JSON en utilisant JsonWriter.
        
        Args:
            file_path: Chemin du fichier à reconstruire
            
        Returns:
            ValidationResult: Résultat de la reconstruction avec statut et backup
        """
        if not file_path.exists():
            return ValidationResult(
                success=False,
                format_type="error",
                message=f"Le fichier {file_path} n'existe pas"
            )

        try:
            # Lecture du contenu actuel
            with open(file_path, 'r', encoding='utf-8') as f:
                content_str = f.read()
                
            # Parse avec notre parseur spécifique
            content, error = parse_starsector_json(content_str)
            if error:
                return ValidationResult(
                    success=False,
                    format_type="error",
                    message=error
                )
            if not content:
                return ValidationResult(
                    success=False,
                    format_type="error",
                    message="Erreur de parsing : contenu vide"
                )

            # Initialisation du writer avec validator
            writer = JsonWriter(validator=JsonValidator())
            
            # Détermination du type de fichier
            file_type = None
            if "strings" in content:
                file_type = JsonFileType.STRINGS
            elif "tips" in content:
                file_type = JsonFileType.TIPS
            elif "codex" in content or "warroom" in content:
                file_type = JsonFileType.TOOLTIPS
            else:
                file_type = JsonFileType.DESCRIPTIONS

            # Validation avant reconstruction
            validator = JsonValidator()
            validation = validator.validate_format(content, file_type)
            if not validation.success:
                return validation

            # Reconstruction avec backup seulement si validation ok
            result = writer.write_json(content, file_path, file_type)
            
            return result

        except Exception as e:
            return ValidationResult(
                success=False,
                format_type="error",
                message=f"Erreur lors de la reconstruction : {str(e)}"
            )

    def rebuild_all_translations(self) -> List[Tuple[Path, bool]]:
        """Reconstruit tous les fichiers traduits dans les dossiers spécifiés."""
        results = []
        
        # Dossiers à scanner
        dirs_to_scan = [
            'data/strings',
            'data/campaign',
            'data/config',
            'data/world',
            'data/characters',
            'data/missions',
            'data/variants'
        ]
        
        # Parcours des dossiers
        for dir_path in dirs_to_scan:
            full_path = self.base_path / dir_path
            if not full_path.exists():
                if self.verbose:
                    logging.info(f"Dossier {dir_path} non trouvé")
                continue
                
            # Scan des fichiers JSON
            for json_file in full_path.glob('*.json'):
                try:
                    # Reconstruction du fichier
                    result = self.rebuild_json_file(json_file)
                    if self.verbose:
                        logging.info(f"Reconstruction de {json_file}: {'✓' if result.success else '✗'}")
                    results.append((json_file, result.success))
                except Exception as e:
                    logging.error(f"Erreur lors de la reconstruction de {json_file}: {str(e)}")
                    results.append((json_file, False))
        
        return results

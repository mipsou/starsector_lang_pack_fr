#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestionnaire de fichiers JSON pour Starsector.
Gère les spécificités du format JSON utilisé par le jeu.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import logging
from tools.fix_quotes import fix_quotes

@dataclass
class ValidationResult:
    """Résultat de validation d'un fichier JSON."""
    success: bool
    format_type: str
    message: str = ""
    
@dataclass
class ComparisonResult:
    """Résultat de comparaison entre deux structures JSON."""
    valid_structure: bool
    identical: bool
    differences: List[str]
    
@dataclass
class VariableValidation:
    """Résultat de validation des variables système."""
    success: bool
    variables: Set[str]
    invalid_vars: Set[str]

class JsonHandler:
    """Gestionnaire de fichiers JSON pour Starsector."""
    
    def __init__(self, logger: logging.Logger):
        """
        Initialise le gestionnaire JSON.
        
        Args:
            logger: Logger pour la journalisation
        """
        self.logger = logger
        self.format_validators = {
            "tips": self._validate_tips_format,
            "tooltips": self._validate_tooltips_format,
            "strings": self._validate_strings_format
        }
        
        # Variables système connues
        self.known_variables = {
            "$faction", "$fleetOrShip", "$playerName",
            "$shipName", "$systemName", "$planetName"
        }
    
    def validate_format(self, file_path: Path) -> ValidationResult:
        """
        Valide le format d'un fichier JSON.
        
        Args:
            file_path: Chemin du fichier à valider
            
        Returns:
            Résultat de la validation
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
            # Détermine le type de format
            format_type = self._detect_format_type(content)
            if not format_type:
                return ValidationResult(False, "", "Format non reconnu")
                
            # Valide avec le validateur approprié
            validator = self.format_validators[format_type]
            is_valid = validator(content)
            
            return ValidationResult(
                success=is_valid,
                format_type=format_type,
                message="Format valide" if is_valid else "Format invalide"
            )
            
        except Exception as e:
            self.logger.error(f"Erreur de validation : {str(e)}")
            return ValidationResult(False, "", f"Erreur : {str(e)}")
    
    def fix_quotes(self, file_path: Path) -> bool:
        """
        Convertit les guillemets droits en guillemets français dans un fichier JSON.
        Préserve le format exact du fichier, y compris les virgules finales.
        
        Args:
            file_path: Chemin du fichier à traiter
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Lit le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fonction pour remplacer les guillemets dans une chaîne
            def replace_quotes(match):
                text = match.group(1)
                # Si le texte contient déjà des guillemets français, on ne fait rien
                if '«' in text or '»' in text:
                    return match.group(0)
                # Sinon, on convertit les guillemets droits en français
                text = text.replace('"', '" ').replace('"', ' "')
                text = text.replace('"', '«').replace('"', '»')
                return f'"{text}"'
            
            # Trouve et remplace les chaînes entre guillemets
            pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"'
            modified = re.sub(pattern, replace_quotes, content)
            
            # Écrit le contenu modifié
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur de normalisation : {str(e)}")
            return False
    
    def write_json(self, file_path: Path, content: dict, starsector_format: bool = True) -> bool:
        """
        Écrit un contenu JSON dans un fichier.
        
        Args:
            file_path: Chemin du fichier
            content: Contenu à écrire
            starsector_format: Si True, utilise le format spécifique de Starsector
            
        Returns:
            True si succès, False sinon
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if starsector_format:
                    # Convertit en JSON avec indentation
                    json_str = json.dumps(content, ensure_ascii=False, indent=4)
                    # Ajoute les virgules finales requises par le format Starsector
                    json_str = re.sub(r'([}\]])(,?\s*[}\]])', r'\1,\2', json_str)
                    f.write(json_str)
                else:
                    json.dump(content, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Erreur d'écriture JSON : {str(e)}")
            return False
    
    def validate_against_original(self, file_path: Path, original: dict) -> ComparisonResult:
        """
        Compare la structure d'un fichier JSON avec l'original.
        
        Args:
            file_path: Chemin du fichier à comparer
            original: Structure originale
            
        Returns:
            Résultat de la comparaison
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            differences = []
            
            def compare_structure(orig, curr, path=""):
                # Si les types sont différents, c'est une erreur de structure
                if type(orig) != type(curr):
                    differences.append(f"Type différent à {path}: {type(orig)} vs {type(curr)}")
                    return False
                
                # Pour les dictionnaires, vérifie les clés
                if isinstance(orig, dict):
                    orig_keys = set(orig.keys())
                    curr_keys = set(curr.keys())
                    
                    if orig_keys != curr_keys:
                        missing = orig_keys - curr_keys
                        extra = curr_keys - orig_keys
                        if missing:
                            differences.append(f"Clés manquantes à {path}: {missing}")
                        if extra:
                            differences.append(f"Clés supplémentaires à {path}: {extra}")
                        return False
                    
                    # Vérifie la structure des sous-éléments
                    return all(compare_structure(orig[k], curr[k], f"{path}.{k}" if path else k)
                             for k in orig_keys)
                
                # Pour les listes, vérifie uniquement la structure
                elif isinstance(orig, list):
                    # Une différence de longueur n'est pas une erreur de structure
                    if len(orig) != len(curr):
                        differences.append(f"Longueur différente à {path}: {len(orig)} vs {len(curr)}")
                    
                    # Vérifie la structure des éléments existants
                    return True
                
                # Pour les types simples, la structure est toujours valide
                return True
            
            # Compare la structure
            valid_structure = compare_structure(original, content)
            
            # Un fichier est identique seulement s'il n'y a aucune différence
            return ComparisonResult(
                valid_structure=valid_structure,
                identical=len(differences) == 0,
                differences=differences
            )
            
        except Exception as e:
            self.logger.error(f"Erreur de comparaison : {str(e)}")
            return ComparisonResult(
                valid_structure=False,
                identical=False,
                differences=[f"Erreur de comparaison : {str(e)}"]
            )

    def validate_variables(self, file_path: Path) -> VariableValidation:
        """
        Valide les variables système dans un fichier.
        
        Args:
            file_path: Chemin du fichier à valider
            
        Returns:
            Résultat de la validation
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Trouve toutes les variables ($xxx)
            variables = set(re.findall(r'\$\w+', content))
            
            # Vérifie les variables inconnues
            invalid_vars = variables - self.known_variables
            
            return VariableValidation(
                success=(len(invalid_vars) == 0),
                variables=variables,
                invalid_vars=invalid_vars
            )
            
        except Exception as e:
            self.logger.error(f"Erreur de validation des variables : {str(e)}")
            return VariableValidation(False, set(), set())
    
    def convert_quotes(self, text):
        """Convertit les guillemets droits en guillemets français avec gestion des guillemets imbriqués.

        Délègue au module tools.fix_quotes qui implémente la conversion récursive
        avec gestion correcte des niveaux d'imbrication.
        """
        from tools.fix_quotes import convert_quotes_starsector

        # Si c'est un fichier, le traiter
        if isinstance(text, Path):
            try:
                with open(text, 'r', encoding='utf-8') as f:
                    content = f.read()
                    try:
                        data = json.loads(content)
                        return self._process_json_data(data)
                    except json.JSONDecodeError:
                        self.logger.error(f"Erreur lors du décodage JSON de {text}")
                        return content
            except Exception as e:
                self.logger.error(f"Erreur lors de la lecture du fichier {text}: {str(e)}")
                return text

        if not text:
            return text

        return convert_quotes_starsector(text)
    
    def _process_json_data(self, data):
        """Traite les données JSON pour convertir les guillemets.
        
        Args:
            data: Les données JSON à traiter
            
        Returns:
            str: Les données JSON avec les guillemets convertis
        """
        if isinstance(data, dict):
            return {k: self._process_json_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_json_data(item) for item in data]
        elif isinstance(data, str):
            # Convertir les guillemets en préservant la structure JSON
            content = data
            
            # Gérer les guillemets échappés
            content = re.sub(r'\\"', r'«', content)  # Remplacer les guillemets échappés par des guillemets français
            
            # Gérer les guillemets non échappés
            content = re.sub(r'"([^"]+)"', r'«\1»', content)
            
            # Ajouter les espaces typographiques
            content = re.sub(r'«\s*([^»]+)\s*»', r'« \1 »', content)
            
            # Nettoyer les espaces multiples
            content = re.sub(r'\s+', ' ', content)
            content = content.strip()
            
            # Gérer les guillemets imbriqués
            content = re.sub(r'»\s*«', r'»«', content)  # Pas d'espace entre guillemets
            content = re.sub(r'«\s*«([^»]+)»\s*»', r'«\1»', content)  # Nettoyer les guillemets imbriqués
            
            # Gérer les espaces avant la ponctuation
            content = re.sub(r'\s+([.,;:!?])', r' \1', content)
            
            return content
        else:
            return data
    
    def _detect_format_type(self, content: dict) -> Optional[str]:
        """Détecte le type de format JSON."""
        if "tips" in content:
            return "tips"
        elif "codex" in content or "combat" in content:
            return "tooltips"
        elif any(isinstance(v, dict) and any('$' in str(x) for x in v.values())
                for v in content.values()):
            return "strings"
        return None
    
    def _validate_tips_format(self, content: dict) -> bool:
        """Valide le format tips.json."""
        if not isinstance(content.get("tips"), list):
            return False
            
        for item in content["tips"]:
            if isinstance(item, dict):
                if not all(k in item for k in ["freq", "tip"]):
                    return False
            elif not isinstance(item, str):
                return False
        
        return True
    
    def _validate_tooltips_format(self, content: dict) -> bool:
        """Valide le format tooltips.json."""
        if "codex" in content:
            if not isinstance(content["codex"], dict):
                return False
            for section in content["codex"].values():
                if not isinstance(section, dict):
                    return False
                if not all(k in section for k in ["title", "body"]):
                    return False
        
        if "combat" in content:
            if not isinstance(content["combat"], list):
                return False
            if not all(isinstance(x, str) for x in content["combat"]):
                return False
        
        return True
    
    def _validate_strings_format(self, content: dict) -> bool:
        """Valide le format strings.json."""
        if not isinstance(content, dict):
            return False
            
        for section in content.values():
            if not isinstance(section, dict):
                return False
            if not all(isinstance(v, str) for v in section.values()):
                return False
        
        return True

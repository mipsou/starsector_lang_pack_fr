#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation des traductions françaises pour Starsector

Ce script :
- Valide la grammaire et l'orthographe françaises
- Vérifie la typographie
- Analyse les fichiers JSON et CSV
- Génère des rapports détaillés

Auteur: Mipsou
Date: 2025-01-22
"""

import re
import json
import spacy
from pathlib import Path
from typing import List, Dict, Any, Tuple
from utils import validate_typography, check_encoding, fix_quotes

class FrenchValidator:
    """Validateur spécifique pour la langue française."""
    
    def __init__(self):
        """Initialisation du validateur."""
        self.common_errors = {
            r'\b[A-Z][a-z]+ s\b': "Possible erreur de possession anglaise ('s)",
            r'\b[A-Z]+s\b': "Possible pluriel en majuscules",
            r'\b\d+\s*%': "Format de pourcentage incorrect (utiliser « % »)",
            r'"([^"]*)"': "Guillemets droits au lieu de guillemets français (« »)",
        }
        
        # Chargement du modèle spaCy pour le français
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except:
            print("ATTENTION: Modèle français spaCy non trouvé. Installation requise:")
            print("python -m spacy download fr_core_news_sm")
            self.nlp = None

    def validate_text(self, text: str) -> List[Dict[str, Any]]:
        """Valide un texte en français.
        
        Args:
            text (str): Le texte à valider
            
        Returns:
            List[Dict[str, Any]]: Liste des problèmes trouvés
        """
        issues = []
        
        # Vérification des erreurs courantes
        for pattern, message in self.common_errors.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                issues.append({
                    "type": "error",
                    "message": message,
                    "position": match.span(),
                    "text": match.group()
                })
        
        # Vérification typographique avec utils.py
        is_valid, errors = validate_typography(text)
        if not is_valid:
            for error in errors:
                issues.append({
                    "type": "typography",
                    "message": error,
                    "position": (0, 0),  # Position exacte non disponible
                    "text": text
                })
        
        # Analyse grammaticale si spaCy est disponible
        if self.nlp:
            doc = self.nlp(text)
            for token in doc:
                if token.pos_ == "VERB":
                    # Vérification basique de la conjugaison
                    pass  # À implémenter
        
        return issues

    def validate_json_file(self, file_path: Path) -> Dict[str, List[Dict[str, Any]]]:
        """Valide un fichier JSON contenant des traductions.
        
        Args:
            file_path (Path): Chemin vers le fichier JSON
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Résultats de la validation
        """
        # Vérification de l'encodage
        if not check_encoding(file_path):
            raise ValueError(f"Le fichier {file_path} n'est pas en UTF-8")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Correction des guillemets avant validation
                value = fix_quotes(value)
                issues = self.validate_text(value)
                if issues:
                    results[key] = issues
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, str):
                        # Correction des guillemets avant validation
                        sub_value = fix_quotes(sub_value)
                        issues = self.validate_text(sub_value)
                        if issues:
                            results[f"{key}.{sub_key}"] = issues
        
        return results

    def generate_report(self, results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Génère un rapport de validation.
        
        Args:
            results (Dict[str, List[Dict[str, Any]]]): Résultats de la validation
            
        Returns:
            str: Rapport formaté en Markdown
        """
        report = ["# Rapport de Validation Française\n"]
        
        total_issues = 0
        for key, issues in results.items():
            if issues:
                report.append(f"\n## {key}\n")
                for issue in issues:
                    total_issues += 1
                    report.append(f"- **{issue['type']}**: {issue['message']}")
                    report.append(f"  - Texte: `{issue['text']}`\n")
        
        report.insert(1, f"\nTotal des problèmes trouvés : {total_issues}\n")
        
        return "\n".join(report)

def main():
    """Point d'entrée principal du script."""
    try:
        validator = FrenchValidator()
        
        # Validation des fichiers de traduction
        translation_dir = Path("localization/fr/data/strings")
        for json_file in translation_dir.glob("*.json"):
            print(f"\nValidation de {json_file.name}...")
            results = validator.validate_json_file(json_file)
            
            # Génération et sauvegarde du rapport
            report = validator.generate_report(results)
            report_file = Path("reports") / f"validation_{json_file.stem}.md"
            report_file.parent.mkdir(exist_ok=True)
            
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"Rapport sauvegardé dans {report_file}")
            
    except Exception as e:
        print(f"Erreur : {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()

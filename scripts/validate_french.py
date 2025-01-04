#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import spacy
from pathlib import Path
from typing import List, Dict, Any

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
        
        self.typography_rules = {
            "spaces": {
                "before": ":;!?»",
                "after": "«",
                "both": ":",
            }
        }
        
        # Chargement du modèle spaCy pour le français
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except:
            print("ATTENTION: Modèle français spaCy non trouvé. Installation requise:")
            print("python -m spacy download fr_core_news_sm")
            self.nlp = None

    def validate_text(self, text: str) -> List[Dict[str, Any]]:
        """Valide un texte en français."""
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
        
        # Vérification typographique
        for char in self.typography_rules["spaces"]["before"]:
            pattern = f"\\S{char}"
            matches = re.finditer(pattern, text)
            for match in matches:
                issues.append({
                    "type": "typography",
                    "message": f"Espace manquant avant '{char}'",
                    "position": match.span(),
                    "text": match.group()
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
        """Valide un fichier JSON contenant des traductions."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {}
        for key, value in data.items():
            if isinstance(value, str):
                issues = self.validate_text(value)
                if issues:
                    results[key] = issues
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, str):
                        issues = self.validate_text(sub_value)
                        if issues:
                            results[f"{key}.{sub_key}"] = issues
        
        return results

    def generate_report(self, results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Génère un rapport de validation."""
        report = ["# Rapport de Validation Française\n"]
        
        for key, issues in results.items():
            if issues:
                report.append(f"\n## {key}\n")
                for issue in issues:
                    report.append(f"- {issue['message']}")
                    report.append(f"  * Texte: {issue['text']}")
                    report.append(f"  * Position: {issue['position']}\n")
        
        return "\n".join(report)

def main():
    """Fonction principale."""
    validator = FrenchValidator()
    base_path = Path("D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private")
    
    # Validation des fichiers de traduction
    translation_files = list(base_path.rglob("*.json"))
    for file in translation_files:
        if "localization/fr" in str(file):
            print(f"\nValidation de {file}")
            results = validator.validate_json_file(file)
            
            # Génération du rapport
            if results:
                report = validator.generate_report(results)
                report_file = base_path / "validation_reports" / f"{file.stem}_report.md"
                report_file.parent.mkdir(exist_ok=True)
                report_file.write_text(report, encoding='utf-8')
                print(f"Rapport généré : {report_file}")
            else:
                print("Aucun problème trouvé.")

if __name__ == "__main__":
    main()

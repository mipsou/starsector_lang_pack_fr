#!/usr/bin/env python3
"""
Script de conversion des fichiers CSV en JSON.
Permet de convertir les fichiers de traduction du format CSV au format JSON.
"""

import csv
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)

class CSVToJSONConverter:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        
    def convert(self) -> bool:
        """Convertit un fichier CSV en JSON."""
        try:
            # Lecture du CSV
            data = self._read_csv()
            
            # Conversion en format JSON
            json_data = self._format_json(data)
            
            # Écriture du fichier JSON
            self._write_json(json_data)
            
            logging.info(f"Conversion réussie : {self.input_file} -> {self.output_file}")
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de la conversion : {str(e)}")
            return False
    
    def _read_csv(self) -> List[Dict[str, str]]:
        """Lit le fichier CSV et retourne les données."""
        data = []
        try:
            with open(self.input_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du CSV : {str(e)}")
            raise
    
    def _format_json(self, data: List[Dict[str, str]]) -> Dict[str, Any]:
        """Formate les données pour le JSON."""
        json_data = {}
        
        # Regroupement par ID si présent
        for row in data:
            if 'id' in row:
                key = row['id']
                # Supprime l'ID du dictionnaire final
                row_data = {k: v for k, v in row.items() if k != 'id'}
                
                # Si une seule valeur reste, utilise la valeur directement
                if len(row_data) == 1:
                    json_data[key] = next(iter(row_data.values()))
                else:
                    json_data[key] = row_data
            else:
                # Sans ID, utilise la première colonne comme clé
                key = next(iter(row.keys()))
                value = row[key]
                json_data[key] = value
        
        return json_data
    
    def _write_json(self, data: Dict[str, Any]) -> None:
        """Écrit les données au format JSON."""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Erreur lors de l'écriture du JSON : {str(e)}")
            raise

def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description='Convertit un fichier CSV en JSON.')
    parser.add_argument('input_file', help='Chemin vers le fichier CSV d\'entrée')
    parser.add_argument('output_file', help='Chemin vers le fichier JSON de sortie')
    args = parser.parse_args()
    
    converter = CSVToJSONConverter(args.input_file, args.output_file)
    success = converter.convert()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())

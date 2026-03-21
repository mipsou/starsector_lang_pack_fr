"""
Script utilitaire de validation JSON (pas un test pytest).
Utilisé manuellement pour valider les fichiers de traduction contre les originaux.
"""

import logging
import json
from pathlib import Path


def main():
    from scripts.handlers.json_handler import JsonHandler

    logger = logging.getLogger('test')
    handler = JsonHandler(logger)

    original_path = Path('d:/Fractal Softworks/Starsector/starsector-core/data/strings/tooltips.json')
    if not original_path.exists():
        print(f"Fichier original non trouvé : {original_path}")
        return

    # Charge le fichier original
    with open(original_path, 'r', encoding='utf-8') as f:
        original = json.load(f)

    # Vérifie le fichier converti
    result = handler.validate_against_original(
        Path('tests/data/tooltips_fr.json'),
        original
    )

    print(f"Structure valide: {result.valid_structure}")
    print(f"Identique: {result.identical}")
    print("\nDifférences:")
    for diff in result.differences:
        print(f"- {diff}")


if __name__ == '__main__':
    main()

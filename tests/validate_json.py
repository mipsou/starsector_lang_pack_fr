import logging
import json
from pathlib import Path
from scripts.handlers.json_handler import JsonHandler

logger = logging.getLogger('test')
handler = JsonHandler(logger)

# Charge le fichier original
with open('starsector-core/data/strings/tooltips.json', 'r', encoding='utf-8') as f:
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

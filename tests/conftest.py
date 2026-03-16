import pytest
import sys
import os
from pathlib import Path

# Répertoire racine du projet
ROOT_DIR = Path(__file__).parent.parent

# Ajouter les répertoires nécessaires au PYTHONPATH
for path_to_add in [str(ROOT_DIR), str(ROOT_DIR / 'scripts'), str(ROOT_DIR / 'tools')]:
    if path_to_add not in sys.path:
        sys.path.insert(0, path_to_add)

# Changer le répertoire de travail vers la racine du projet
# pour que les chemins relatifs dans les tests fonctionnent correctement
os.chdir(str(ROOT_DIR))

# Guide d'Installation pour Développeurs

## Prérequis
- Python 3.10+
- Git
- Éditeur de texte avec support UTF-8
- Starsector installé

## Installation

1. Cloner le repository
```bash
git clone https://github.com/votre-compte/starsector_lang_pack_fr.git
cd starsector_lang_pack_fr
```

2. Installer les dépendances
```bash
pip install -r tests/requirements.txt
```

3. Configurer l'environnement
```bash
# Créer les dossiers nécessaires
mkdir -p data/config data/strings
```

4. Vérifier l'installation
```bash
python tools/validate_translations.py
python -m pytest
```

## Structure du Projet
```
starsector_lang_pack_fr/
├── data/
│   ├── config/    # Fichiers de configuration
│   └── strings/   # Fichiers de traduction
├── docs/         # Documentation
├── tests/        # Tests automatisés
└── tools/        # Scripts utilitaires
```

## Workflow de Développement

1. Créer une branche
```bash
git checkout -b feature/ma-traduction
```

2. Mettre à jour les traductions
```bash
python tools/update_translations.py
```

3. Valider les modifications
```bash
python tools/validate_translations.py
python -m pytest
```

4. Commiter les changements
```bash
git add .
git commit -m "feat: ajout de nouvelles traductions"
```

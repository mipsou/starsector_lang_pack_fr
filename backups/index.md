# Index des Backups

## Vue d'Ensemble
- Taille totale : 814,502 octets (~795 Ko)
- Nombre total de fichiers : 69
- Date de dernière mise à jour : 2025-02-02

## Structure
```
backups/
├── docs_20250201/        # Documentation (5 fichiers)
├── missions/            # 15 missions avec traductions
├── requirements_20250104/ # Dépendances (1 fichier)
├── strings_20250104/    # Traductions v1 (7 fichiers)
├── strings_20250131/    # Traductions v2 (12 fichiers)
├── tests_20250202/     # Suite de tests (13 fichiers)
└── tips_20250131/      # Messages d'aide (15 fichiers)
```

## Contenu par Répertoire

### 📚 Documentation (docs_20250201/)
- Backups du CDC et DEVBOOK
- Format : fichier.md.backup_YYYYMMDD_HHMMSS
- [Détails](docs_20250201/index.md)

### 🎮 Missions (missions/)
- 15 missions du jeu
- Une traduction par mission
- [Détails](missions/index.md)

### 📋 Requirements (requirements_20250104/)
- Dépendances du projet
- Version de référence : 4 janvier 2025
- [Détails](requirements_20250104/index.md)

### 🔤 Traductions (strings_*)
- Version 20250104 : première version
- Version 20250131 : version actuelle (422 lignes)
- [Détails v1](strings_20250104/index.md)
- [Détails v2](strings_20250131/index.md)

### 🧪 Tests (tests_20250202/)
- 10 fichiers de test spécialisés
- 3 fichiers utilitaires
- [Détails](tests_20250202/index.md)

### 💡 Tips (tips_20250131/)
- Messages d'aide et conseils
- 15 versions successives
- [Détails](tips_20250131/index.md)

## Convention de Nommage
- Répertoires : `type_YYYYMMDD`
- Fichiers : `nom.extension.backup_YYYYMMDD_HHMMSS`
- Index : `index.md` dans chaque répertoire

## Notes
- Chaque répertoire contient son propre index.md
- Les liens pointent vers les détails spécifiques
- Structure maintenue pour faciliter la recherche et restauration

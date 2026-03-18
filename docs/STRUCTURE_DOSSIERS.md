# Structure des Dossiers

## Organisation Actuelle

```
starsector_lang_pack_fr_private/
├── backups/               # Sauvegardes des fichiers modifiés
├── data/                  # Données du mod
├── docs/                  # Documentation du projet
├── localization/          # Fichiers de traduction
├── localization.old/      # Ancienne version (à nettoyer)
├── logs/                  # Journaux d'exécution
├── original/             # Fichiers originaux de référence
├── original.old/         # Ancienne version (à nettoyer)
├── requirements/         # Dépendances Python par environnement
├── scripts/             # Scripts Python principaux
├── temp/                # Fichiers temporaires
├── tests/              # Tests unitaires et d'intégration
└── tools/              # Outils et utilitaires
```

## Structure Proposée

```
starsector_lang_pack_fr_private/
├── backups/                    # Sauvegardes organisées par date
│   └── YYYYMMDD_HHMMSS/       # Un dossier par sauvegarde
├── data/                      # Données du mod
│   ├── config/               # Configuration du mod
│   └── content/             # Contenu spécifique
├── docs/                    # Documentation
│   ├── api/                # Documentation API
│   ├── dev/               # Documentation développeur
│   └── user/              # Documentation utilisateur
├── localization/          # Fichiers de traduction
│   ├── data/             # Données de traduction
│   └── temp/             # Fichiers temporaires de traduction
├── logs/                 # Journaux d'exécution
│   ├── builds/          # Logs de construction
│   └── runs/            # Logs d'exécution
├── original/           # Fichiers originaux (référence)
│   └── versions/       # Versions spécifiques
├── scripts/           # Scripts Python
│   ├── core/         # Fonctionnalités principales
│   ├── handlers/     # Gestionnaires spécifiques
│   ├── tools/        # Outils et utilitaires
│   └── utils/        # Fonctions utilitaires
└── tests/           # Tests
    ├── data/        # Données de test
    ├── integration/ # Tests d'intégration
    └── unit/        # Tests unitaires
```

## Actions de Migration

### 1. Nettoyage
- [ ] Supprimer `localization.old/`
- [ ] Supprimer `original.old/`
- [ ] Nettoyer `temp/`

### 2. Réorganisation
- [ ] Créer la nouvelle structure
- [ ] Migrer les fichiers
- [ ] Mettre à jour les chemins

### 3. Documentation
- [ ] Documenter chaque dossier
- [ ] Mettre à jour les références
- [ ] Valider la cohérence

## Notes
- Garder une copie de sauvegarde avant migration
- Tester les scripts après déplacement
- Mettre à jour les imports Python

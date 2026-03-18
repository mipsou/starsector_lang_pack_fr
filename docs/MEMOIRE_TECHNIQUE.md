# Mémoire Technique du Projet

## Structure de la Documentation

### 1. Formats de Fichiers
- `FORMATS_JSON.md` : Documentation des structures JSON
- `REFERENCE_ENCODAGE.md` : Guide d'encodage UTF-8
- `LOG_ANALYSIS.md` : Analyse des logs Starsector

### 2. Rapports
- `RAPPORT_YYYY_MM_DD.md` : Rapports journaliers
- Stockés dans `/docs/rapports/` (à créer)

### 3. Journal de Développement
- `DEVBOOK.md` : Journal quotidien des modifications
- Focus sur les actions et décisions

## Organisation des Connaissances

### Standards Techniques
1. **Encodage**
   - UTF-8 pour tous les fichiers
   - Pas de BOM
   - Support complet des accents

2. **Format JSON**
   - Trois structures validées (voir FORMATS_JSON.md)
   - Variables système préservées
   - Indentation cohérente

3. **Logs**
   - Commandes PowerShell validées
   - Analyse structurée
   - Points de contrôle identifiés

### Workflow
1. **Modifications**
   - Toujours vérifier avant de modifier
   - Créer une sauvegarde si nécessaire
   - Documenter dans le DEVBOOK

2. **Documentation**
   - Rapports journaliers
   - Mise à jour du DEVBOOK
   - Documentation technique séparée

3. **Validation**
   - Tests d'encodage
   - Vérification des formats
   - Contrôle des variables système

## Gestion des Fichiers JSON

### 1. Règles Fondamentales
- ⛔ JAMAIS utiliser `import json`
- ✅ TOUJOURS utiliser `format_starsector_json` et `parse_starsector_json`
- 🔒 TOUJOURS valider avant écriture

### 2. Types de Fichiers
```python
class FileType(Enum):
    STRINGS = 1    # strings.json
    TIPS = 2       # tips.json
    TOOLTIPS = 3   # tooltips.json
    DESCRIPTIONS = 4 # descriptions.json
```

### 3. Workflow de Modification
1. Validation Initiale
   ```python
   validation = validator.validate_format(content, file_type)
   if not validation.success:
       return validation
   ```

2. Création Backup
   ```python
   backup = writer.create_backup(file_path)
   ```

3. Écriture Sécurisée
   ```python
   formatted = format_starsector_json(content, file_type)
   with open(file_path, "w", encoding="utf-8") as f:
       f.write(formatted)
   ```

### 4. Validation des Formats
Chaque type de fichier a ses propres règles :

1. **strings.json**
   - Structure hiérarchique
   - Clé "strings" obligatoire
   - Variables $faction, $market

2. **tips.json**
   - Structure en tableau
   - Variable $market
   - Mélange strings/objets

3. **tooltips.json**
   - Structure hiérarchique
   - Sections codex/warroom
   - Variables $damage, $flux

4. **descriptions.json**
   - Structure en tableau
   - Champs obligatoires : key, original, translation, stage
   - Variables $damage, $faction, $market

### 5. Gestion des Erreurs
1. Création systématique de REX
2. Documentation dans DEVBOOK.md
3. Mise à jour des procédures

### 6. Tests
1. Tests unitaires par format
2. Tests d'intégration workflow
3. Tests variables système

### 7. Documentation
- FORMATS_JSON.md : référence des formats
- DEVBOOK.md : historique modifications
- REX : retours d'expérience

## Fichiers Originaux

### Structure
Le dossier `original/` est une copie exacte de `starsector-core/data/` et sert de référence pour la traduction.

### Hiérarchie
```
original/
├── data/
│   ├── strings/
│   │   ├── strings.json
│   │   ├── tips.json
│   │   └── tooltips.json
│   └── ...
└── jar_extract/
```

### Utilisation
1. Source de vérité pour les formats
2. Base pour la traduction
3. Référence pour les tests

### Maintenance
- Vérifier régulièrement la synchronisation avec starsector-core
- Ne jamais modifier les fichiers originaux
- Utiliser comme référence pour la validation

## Maintenance

### Organisation des Fichiers
```
/docs/
  ├── DEVBOOK.md           # Journal de développement
  ├── MEMOIRE_TECHNIQUE.md # Ce document
  ├── FORMATS_JSON.md      # Documentation JSON
  ├── LOG_ANALYSIS.md      # Analyse des logs
  └── rapports/           # Rapports journaliers
      └── RAPPORT_YYYY_MM_DD.md
```

### Mises à Jour
1. Documenter les nouvelles découvertes
2. Mettre à jour les références
3. Archiver les anciens rapports

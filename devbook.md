# Guide de Développement - Starsector Language Pack FR

## Environnement de Développement

### Structure des Dossiers
```
starsector_lang_pack_fr/
├── mod_info.json
└── localization/
    ├── data/
    │   ├── config/     # Configurations localisées
    │   └── strings/    # Fichiers de traduction
    └── graphics/
        └── ui/        # Éléments d'interface traduits
```

### Outils Nécessaires
- Éditeur de texte avec support UTF-8
- Git pour le versioning
- Python pour les scripts d'automatisation
- Starsector pour les tests

## Processus de Développement

### 1. Configuration Initiale
1. Cloner le repository
2. Installer les dépendances Python
3. Configurer l'environnement de développement

### 2. Workflow de Traduction
1. Identifier les fichiers à traduire
2. Créer les fichiers _fr correspondants
3. Traduire le contenu
4. Tester en jeu
5. Valider et commiter

### 3. Tests
- Vérifier l'encodage des fichiers
- Tester les caractères spéciaux
- Vérifier l'intégration en jeu
- Valider les performances

## Standards de Code

### Fichiers de Traduction
- Format CSV :
  ```csv
  id,text
  ship_name,"Nom du vaisseau"
  ```
- Format JSON :
  ```json
  {
    "key": "valeur traduite"
  }
  ```

### Conventions de Nommage
- Fichiers : `nom_original_fr.extension`
- Variables : camelCase
- Constantes : UPPER_CASE

## Scripts d'Automatisation

### convert_csv_to_json.py
```python
# Convertit les fichiers CSV en JSON
# Usage : python convert_csv_to_json.py input.csv output.json
```

### validate_translations.py
```python
# Vérifie la validité des traductions
# Usage : python validate_translations.py dir_path
```

## Gestion des Ressources

### Fichiers Graphiques
- Formats supportés : PNG, JPG
- Résolution identique aux originaux
- Nommage cohérent avec le jeu

### Fichiers de Configuration
- Toujours en UTF-8
- Structure JSON valide
- Documentation des changements

## Débogage

### Logs
- Activer les logs de développement
- Vérifier starsector.log
- Utiliser les outils de debug du jeu

### Problèmes Courants
1. Encodage incorrect
   - Solution : Vérifier UTF-8 avec/sans BOM
2. Fichiers manquants
   - Solution : Vérifier la structure
3. Erreurs de syntaxe
   - Solution : Valider JSON/CSV

## Optimisation

### Performance
- Minimiser la taille des fichiers
- Éviter les duplications
- Structurer efficacement

### Maintenance
- Documenter les changements
- Suivre les versions du jeu
- Maintenir la cohérence

## Versioning

### Git
- Une branche par fonctionnalité
- Commits atomiques
- Messages descriptifs

### Releases
- Semantic Versioning
- Notes de version détaillées
- Tests complets

## Documentation

### Commentaires
```python
# TODO: Format standard
# FIXME: Pour les bugs
# NOTE: Informations importantes
```

### Markdown
- README.md : Vue d'ensemble
- CDC.md : Spécifications
- CHANGELOG.md : Modifications
- devbook.md : Guide technique

## Ressources

### Liens Utiles
- [Documentation Starsector](http://fractalsoftworks.com/docs)
- [Wiki Modding](http://starsector.wikia.com/wiki/Modding)
- [Forum Officiel](http://fractalsoftworks.com/forum)

### Références
- Mod chinois : Structure et organisation
- Autres mods de traduction
- Documentation officielle

## Notes de Développement

### Priorités
1. Stabilité du mod
2. Qualité des traductions
3. Performance
4. Maintenance

### À Faire
- [ ] Automatisation complète
- [ ] Tests unitaires
- [ ] Documentation API
- [ ] Outils de validation

## Support

### Contact
- GitHub Issues
- Forum Starsector
- Discord communautaire

### Contribution
1. Fork le projet
2. Créer une branche
3. Commiter les changements
4. Soumettre une PR

## Annexes

### Templates
- Pull Request
- Issue
- Documentation
- Release Notes

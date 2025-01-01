# Guide de Style et Bonnes Pratiques

## Format des Fichiers

### JSON
- Indentation : 4 espaces
- Encodage : UTF-8
- Ordre alphabétique des clés
- Pas de commentaires

### CSV
- Séparateur : virgule (,)
- Encodage : UTF-8
- Guillemets doubles pour les textes
- Une ligne par entrée

## Conventions de Nommage

### Fichiers
- Suffixe `_fr` pour les traductions
- Tout en minuscules
- Séparateurs avec underscore (_)

### Variables
- Descriptives et en français
- CamelCase pour les clés JSON
- snake_case pour les variables Python

## Traduction

### Style
- Formel mais pas pompeux
- Cohérent avec l'univers du jeu
- Adaptation culturelle appropriée

### Ponctuation
- Espaces insécables avant : ; ! ?
- Guillemets français « »
- Points de suspension (…)

### Termes Techniques
- Glossaire commun
- Cohérence des traductions
- Documentation des choix

## Tests

### Avant Commit
1. Vérifier l'encodage
2. Valider le format
3. Tester en jeu
4. Exécuter les tests unitaires

### Qualité
- Pas de texte hardcodé
- Documentation à jour
- Tests pour chaque modification

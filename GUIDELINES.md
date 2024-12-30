# Guidelines de Traduction 🌍

## Principes Généraux

### 1. Cohérence
- Utiliser une terminologie cohérente
- Maintenir le même niveau de langue
- Respecter le glossaire du projet

### 2. Fidélité
- Rester fidèle au sens original
- Adapter les expressions idiomatiques
- Préserver le ton et le style

### 3. Lisibilité
- Phrases claires et concises
- Ponctuation française
- Éviter les anglicismes

## Format des Fichiers

### 1. JSON
```json
{
    "key": "Traduction en français",
    "context": "Contexte d'utilisation",
    "original": "Original text in English"
}
```

### 2. CSV
```csv
id,fr,en
key,"Traduction en français","Original text in English"
```

## Règles Spécifiques

### 1. Noms Propres
- Ne pas traduire les noms de personnages
- Ne pas traduire les noms de vaisseaux
- Traduire les noms de lieux si pertinent

### 2. Termes Techniques
- Utiliser le glossaire officiel
- Maintenir la cohérence avec l'UI
- Documenter les nouveaux termes

### 3. Variables
- Ne pas traduire les variables `{0}`, `{1}`, etc.
- Respecter l'ordre des variables
- Vérifier le contexte d'utilisation

## Processus de Traduction

### 1. Préparation
1. Lire le texte original
2. Comprendre le contexte
3. Identifier les termes techniques

### 2. Traduction
1. Première traduction
2. Révision personnelle
3. Vérification des guidelines

### 3. Validation
1. Relecture par un pair
2. Tests en jeu
3. Validation finale

## Contrôle Qualité

### 1. Vérifications
- Orthographe et grammaire
- Cohérence terminologique
- Format des fichiers

### 2. Tests
- Validation in-game
- Vérification des variables
- Tests de mise en page

### 3. Documentation
- Mettre à jour le glossaire
- Noter les cas particuliers
- Documenter les décisions

## Outils Recommandés

### 1. Éditeurs
- Visual Studio Code avec plugins
- Notepad++ pour édition rapide
- Éditeurs JSON/CSV dédiés

### 2. Vérification
- Correcteur orthographique
- Outils de validation JSON/CSV
- Scripts de vérification

### 3. Ressources
- [Le Grand Robert](https://grandrobert.lerobert.com/)
- [FranceTerme](http://www.culture.fr/franceterme)
- [Glossaire du projet](./docs/glossary.md)

## Processus de Contribution

### 1. Branches
1. Créer une branche depuis `dev`
2. Nommer : `trad/[section]-[description]`
3. Une branche par section

### 2. Commits
1. Format : `trad(scope): message`
2. Description claire et concise
3. Référencer les issues

### 3. Pull Requests
1. Remplir le template
2. Attendre la revue
3. Appliquer les corrections

## Contact

Pour toute question :
1. Ouvrir une issue
2. Contacter l'équipe
3. Consulter le DEVBOOK.md

# Variables Système dans les Fichiers de Traduction

## Variables Identifiées

### Flottes et Vaisseaux
- `$fleetOrShip` : Référence à la flotte ou au vaisseau (selon le contexte)
- `$playerFleetOrShip` : Flotte ou vaisseau du joueur
- `$boardableShipName` : Nom d'un vaisseau abordable

### Factions
- `$faction` : Faction concernée
- `$enemyFactionAndTheirAllies` : Faction ennemie et leurs alliés

### États et Conditions
- `$yourForcesWereOrYourSideWas` : État des forces du joueur
- `$planetName` : Nom de la planète

## Utilisation dans les Fichiers

### strings.json
```json
{
    "initialAggressive": "La $faction $fleetOrShip manœuvre...",
    "approach": "Votre $fleetOrShip approche de $planetName."
}
```

## Règles d'Utilisation
1. Ne jamais traduire les variables (garder le préfixe $)
2. Maintenir l'espace avant et après la variable
3. Respecter la casse exacte des variables
4. Ne pas modifier la structure des phrases contenant des variables

## Vérification
Pour vérifier la cohérence des variables :
1. Chercher avec grep : `\$[a-zA-Z]`
2. Vérifier que chaque variable est utilisée correctement
3. S'assurer que la grammaire est correcte autour des variables

## Test des Variables
Pour tester une traduction avec variables :
1. Remplacer chaque variable par un exemple
2. Vérifier que la phrase reste correcte
3. Tester avec différentes combinaisons

## Notes Importantes
- Les variables sont sensibles à la casse
- Certaines variables peuvent apparaître plusieurs fois dans une même phrase
- La ponctuation doit être cohérente autour des variables

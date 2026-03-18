# Format CSV dans Starsector

## Structure Générale

### Format des Clés
```
descriptions.csv#('id', 'type')$field
```

- `id` : Identifiant unique de l'entrée (ex: 'damage_kinetic', 'astral')
- `type` : Type d'entrée (ex: 'WEAPON', 'SHIP', 'CUSTOM')
- `field` : Champ spécifique (ex: 'text1', 'text2', 'text3')

### Types d'Entrées
1. `WEAPON` : Armes et systèmes d'armement
2. `SHIP` : Vaisseaux et systèmes de vaisseaux
3. `CUSTOM` : Éléments personnalisés
4. `RESOURCE` : Ressources et matériaux
5. `SHIP_SYSTEM` : Systèmes de vaisseaux spécifiques
6. `ASTEROID` : Objets spatiaux

### Champs Standards
1. `text1` : Description principale
2. `text2` : Information secondaire (ex: type d'arme)
3. `text3` : Description courte ou tooltip
4. `text4` : Information additionnelle

## Variables Système

### Variables de Faction
- `$faction` : Nom de la faction actuelle
- `$theFaction` : "la/le" + nom de faction
- `$Faction` : Nom de faction avec majuscule
- `$TheFaction` : "La/Le" + nom de faction

### Variables de Marché
- `$market` : Nom du marché/colonie
- `$theMarket` : "le" + nom du marché
- `$Market` : Nom du marché avec majuscule
- `$TheMarket` : "Le" + nom du marché

### Variables de Combat
- `$damage` : Valeur de dégâts
- `$flux` : Valeur de flux
- `$range` : Portée
- `$time` : Durée

## Exemples

### Arme (WEAPON)
```json
{
    "key": "descriptions.csv#('arbalest', 'WEAPON')$text1",
    "original": "An antiquated weapon design with high per-shot damage...",
    "translation": "Une conception d'arme ancienne avec des dégâts élevés...",
    "stage": 5,
    "context": "Version 0.97a - Arbalest Weapon"
}
```

### Vaisseau (SHIP)
```json
{
    "key": "descriptions.csv#('astral', 'SHIP')$text1",
    "original": "A technologically advanced capital ship...",
    "translation": "Un vaisseau capital technologiquement avancé...",
    "stage": 1,
    "context": "Version 0.97a - Astral Carrier"
}
```

## Bonnes Pratiques

### Traduction
1. Respecter le formatage du texte original (retours à la ligne, espaces)
2. Conserver les variables système telles quelles
3. Maintenir la cohérence des termes techniques
4. Utiliser le contexte pour comprendre le sens

### Validation
1. Vérifier la structure de la clé
2. Valider le format JSON
3. Tester avec les variables système
4. Contrôler les retours à la ligne

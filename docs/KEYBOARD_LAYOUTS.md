# Dispositions de Clavier Supportées

Ce document décrit les équivalences de touches entre les différentes dispositions de clavier supportées par le mod de traduction française de Starsector.

## Touches de Déplacement

| Action | QWERTY | AZERTY | BÉPO |
|--------|--------|--------|------|
| Avancer | W | Z | É |
| Reculer | S | S | U |
| Gauche | A | Q | A |
| Droite | D | D | I |

## Touches d'Action

| Action | QWERTY | AZERTY | BÉPO |
|--------|--------|--------|------|
| Interaction | E | E | E |
| Armes | Q | A | À |
| Bouclier | F | F | F |
| Boost | Shift | Maj | Maj |
| Pause | Space | Espace | Espace |
| Menu | Tab | Tab | Tab |
| Visée | T | T | T |

## Touches de Combat

| Action | QWERTY | AZERTY | BÉPO |
|--------|--------|--------|------|
| Missiles | R | R | R |
| Système | V | V | V |
| Ordres | B | B | B |

## Notes d'Implémentation

1. Les touches spéciales (Espace, Tab, Maj) sont traduites en français mais conservent leur fonction.
2. Les touches de combat (F, R, V, B) restent identiques sur toutes les dispositions pour maintenir la cohérence.
3. Les touches de déplacement sont adaptées pour chaque disposition afin de préserver l'ergonomie.

## Utilisation dans les Scripts

Les scripts de traduction adaptent automatiquement les touches mentionnées dans les conseils et descriptions selon la disposition choisie. Par exemple :

```python
# Exemple d'adaptation des touches
text = "Press W to move forward"

# AZERTY
text_azerty = "Appuyez sur Z pour avancer"

# BÉPO
text_bepo = "Appuyez sur É pour avancer"
```

## Configuration

La disposition du clavier peut être configurée dans les paramètres du mod. Par défaut, la disposition AZERTY est utilisée pour la traduction française.

Pour changer la disposition :

1. Ouvrez le fichier de configuration du mod
2. Modifiez la valeur de `keyboard_layout` :
   - `qwerty` : Disposition QWERTY (par défaut en anglais)
   - `azerty` : Disposition AZERTY (français)
   - `bepo` : Disposition BÉPO (français ergonomique)

## Tests et Validation

Les scripts incluent des tests unitaires pour valider l'adaptation des touches pour chaque disposition :

- Test des touches de déplacement
- Test des touches spéciales
- Test des combinaisons de touches
- Test des messages d'erreur pour les dispositions invalides

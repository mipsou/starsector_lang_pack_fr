# Formats JSON Identifiés

## 1. Format Tips (tips.json)
```json
{
    "tips": [
        {"freq":0, "tip":"Texte avec fréquence"},
        "Texte simple"
    ]
}
```
**Caractéristiques :**
- Tableau simple de strings ou d'objets
- Format le plus simple
- Pas de nesting profond

## 2. Format Tooltips (tooltips.json)
```json
{
    "codex": {
        "damage_kinetic": {
            "title": "Dégâts Cinétiques",
            "body": "Description des dégâts"
        }
    },
    "combat": {
        "tooltipCrashMothball": "Texte simple"
    }
}
```
**Caractéristiques :**
- Structure hiérarchique à 2-3 niveaux
- Objets avec title/body pour certaines sections
- Strings simples pour d'autres sections

## 3. Format Strings (strings.json)
```json
{
    "fleetInteractionDialog": {
        "initialWithStationVsLargeFleet": "Texte avec variables $faction $fleetOrShip",
        "initialAggressive": "Autre texte avec variables"
    }
}
```
**Caractéristiques :**
- Structure hiérarchique à 2 niveaux
- Variables avec préfixe $ dans le texte
- Pas de sous-objets title/body

## 4. Format Descriptions (descriptions.json)
```json
[
    {
        "key": "descriptions.csv#('weapon_name', 'WEAPON')$text1",
        "original": "Description originale avec $damage",
        "translation": "Traduction avec $damage",
        "stage": 1,
        "context": "Contexte de traduction"
    }
]
```
**Caractéristiques :**
- Structure en tableau racine (pas d'objet)
- Chaque élément contient :
  * key : identifiant unique
  * original : texte source
  * translation : texte traduit
  * stage : état de la traduction
  * context : contexte optionnel
- Variables système supportées

## Points Communs
1. Tous utilisent l'UTF-8
2. Tous supportent les accents français
3. Tous utilisent des guillemets droits (")
4. Tous respectent la syntaxe JSON standard

## Différences Clés
1. **Profondeur de Structure :**
   - Tips : 1 niveau
   - Strings : 2 niveaux
   - Tooltips : 2-3 niveaux
   - Descriptions : 1 niveau (tableau)

2. **Format des Valeurs :**
   - Tips : mélange strings/objets dans un tableau
   - Strings : uniquement des strings avec variables
   - Tooltips : mélange strings/objets title-body
   - Descriptions : objets avec clés spécifiques

3. **Variables :**
   - Tips : pas de variables
   - Strings : variables avec $
   - Tooltips : pas de variables
   - Descriptions : variables système supportées

## Règles de Validation

### 1. Validation Structurelle
- Chaque type de fichier a sa propre structure
- Les champs requis doivent être présents
- Les types de données doivent être respectés

### 2. Variables Système
Compatibilité des variables par type :
- **strings.json** : $faction, $market
- **tips.json** : $market
- **tooltips.json** : $damage, $flux
- **descriptions.json** : $damage, $faction, $market

### 3. Règles Communes
1. Encodage
   - TOUJOURS utiliser UTF-8
   - JAMAIS utiliser d'autres encodages

2. Formatage
   - Indentation : 4 espaces
   - Pas de tabulations
   - Pas de BOM

3. Sécurité
   - JAMAIS utiliser json standard
   - TOUJOURS utiliser format_starsector_json()
   - TOUJOURS valider avant écriture

### 4. Procédure de Modification
1. Validation initiale
2. Création backup
3. Modification
4. Validation finale
5. Écriture

## Notes Importantes
- Ne jamais modifier manuellement
- Toujours utiliser les outils validés
- Vérifier la structure avant commit
- Documenter tout changement de format

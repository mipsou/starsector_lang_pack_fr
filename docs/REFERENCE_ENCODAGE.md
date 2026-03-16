# Référence d'Encodage

## Formats de Fichiers

### JSON
- Encodage: UTF-8
- Sauts de ligne: Unix (\n)
- Indentation: 4 espaces
- Guillemets: droits (") uniquement
- Pas d'espace après les deux points dans les clés
- Exemple:
  ```json
  {
    "tips":[
        {"freq":1,"tip":"Exemple de conseil"},
        "Conseil simple"
    ]
  }
  ```

### Missions
- Encodage: UTF-8
- Structure:
  ```
  Lieu: Base Alpha
  Date: 3014
  Objectifs: Défendre la station
  Description: Une mission de défense.
  ```
- Ponctuation française:
  - Point-virgule (;) : espace avant et après
  - Point d'exclamation (!) : espace avant et après
  - Point d'interrogation (?) : espace avant et après
  - Guillemets : pas d'espace à l'intérieur

### CSV
- Encodage: UTF-8
- Séparateur: virgule (,)
- Guillemets: optionnels sauf si nécessaire
- Exemple:
  ```csv
  id,fr,en
  weapon_1,"Canon laser","Laser cannon"
  ```

## Tests de Validation
- Vérification de l'encodage UTF-8
- Validation de la structure JSON
- Contrôle de la typographie française
- Comparaison avec les fichiers originaux

## Outils
- `validate_json()` : Validation des fichiers JSON
- `validate_mission_text()` : Validation des fichiers mission
- `check_encoding()` : Vérification de l'encodage
- `auto_correct_text()` : Correction automatique

## Caractéristiques d'un Encodage Correct
1. Les guillemets sont droits : "exemple"
2. Les apostrophes sont droites : 'exemple'
3. Pas de caractères parasites (Ã, Â, etc.)
4. Espaces simples
5. Retours à la ligne propres

## Test d'Encodage
Pour vérifier si un fichier est correctement encodé :
1. Les accents doivent être lisibles : é, è, à, ù
2. Les caractères spéciaux doivent être nets : ç, œ, æ
3. La ponctuation doit être claire : « » … '

## Caractéristiques du Format des Tips
1. Fichier encodé en UTF-8
2. Structure JSON simple
3. Mélange possible de strings simples et d'objets
4. Pas d'échappement spécial pour les accents
5. Guillemets droits (")
6. Virgules comme séparateurs

## Éléments Validés
- Accents : é, è, à, ù
- Guillemets dans le texte : utiliser \"
- Apostrophes : utiliser '
- Caractères spéciaux : ç, œ

## Application aux Autres Fichiers
Pour adapter ce format :
1. Vérifier l'encodage UTF-8
2. Utiliser la même structure JSON simple
3. Éviter les caractères d'échappement complexes
4. Maintenir une indentation cohérente

## Problèmes Rencontrés

### Encodage Multiple
- Certains caractères sont encodés plusieurs fois
- Exemple : 'é' → 'Ãé' → 'ÃƒÂé'

### Causes Possibles
1. Manipulation du fichier avec différents encodages
2. Conversion automatique incorrecte
3. Copier-coller depuis différentes sources

## Solutions

### 1. Prévention
- Toujours utiliser UTF-8 pour les nouveaux fichiers
- Configurer l'éditeur pour détecter l'encodage
- Vérifier l'encodage avant chaque modification

### 2. Correction
- Utiliser un fichier de référence correctement encodé
- Comparer byte par byte pour détecter les différences
- Appliquer les corrections de manière systématique

### 3. Validation
- Tests automatisés pour vérifier l'encodage
- Vérification visuelle des caractères spéciaux
- Documentation des modifications d'encodage

## Caractères Spéciaux Français

### Ligatures
- `œ` : ligature oe (œuf, cœur)
- `æ` : ligature ae (æther, ex æquo)
- `Œ` : ligature OE majuscule
- `Æ` : ligature AE majuscule

### Diacritiques
- Tréma (¨) : 
  - ë (poëte, Noël)
  - ï (naïf, maïs)
  - ü (ambiguë)
  - ÿ (polyglotte)
- Autres :
  - é, è, ê (été, père, être)
  - à, â (là, pâte)
  - ù, û (où, sûr)
  - ô (côte)
  - î (île)

### Validation
Pour vérifier la présence de ces caractères :
```python
special_chars = {
    'œ': 'oe',  # ligature oe
    'æ': 'ae',  # ligature ae
    'Œ': 'OE',  # ligature OE majuscule
    'Æ': 'AE',  # ligature AE majuscule
    'ë': 'e',   # e tréma
    'ï': 'i',   # i tréma
    'ü': 'u',   # u tréma
    'ÿ': 'y'    # y tréma
}
```

### Exemples
```json
{
    "tips":[
        {"freq":1,"tip":"Le cœur du réacteur"},
        {"freq":1,"tip":"Une ambiguïté dans les données"},
        {"freq":1,"tip":"L'Æther spatial"}
    ]
}
```

## Gestion des Erreurs

### Types d'Erreurs
1. **Erreurs d'Encodage**
   - Encodage non UTF-8
   - Caractères invalides
   - BOM manquant ou incorrect

2. **Erreurs de Format**
   - JSON invalide
   - CSV malformé
   - Structure de mission incorrecte

3. **Erreurs de Contenu**
   - Caractères spéciaux non supportés
   - Typographie incorrecte
   - Ponctuation invalide

### Format des Messages d'Erreur
```python
{
    'message': "Description de l'erreur",
    'file_type': "Type de fichier (json, csv, mission)",
    'section': "Section concernée",
    'line': "Numéro de ligne"
}
```

### Exemple d'Utilisation
```python
try:
    is_valid, errors = validate_with_context(text, {
        'type': 'json',
        'section': 'tips'
    })
    if not is_valid:
        print(format_validation_errors(errors))
except ValidationError as e:
    print(f"Erreur critique : {e}")
    for error in e.errors:
        print(f"- {error}")
```

### Bonnes Pratiques
1. Toujours spécifier le contexte de validation
2. Utiliser try/except pour gérer les erreurs critiques
3. Formater les erreurs de manière lisible
4. Inclure les numéros de ligne quand possible

## Outils

### Scripts Python
```python
def load_json_file(file_path, encodings=['utf-8', 'latin1', 'cp1252']):
    """Charge un fichier JSON en essayant différents encodages."""
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise ValueError(f"Impossible de lire le fichier avec les encodages {encodings}")
```

### Tests
```python
def test_file_encoding():
    """Vérifie l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        content = f.read()
    assert b'Ã' not in content, "Encodage incorrect détecté"
```

## Références

### Encodages Courants
- UTF-8 : Encodage universel recommandé
- Latin1 : Encodage historique européen
- CP1252 : Encodage Windows pour l'Europe occidentale

### Caractères Spéciaux Français
- é, è, à, â, ê, î, ô, û (accents)
- ç (cédille)
- œ (ligature)
- « » (guillemets français)
- Points de suspension (…)

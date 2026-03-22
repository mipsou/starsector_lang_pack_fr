# PLAN TRADUCTION RULES.CSV — PIPELINE DÉFENSIF

## Architecture : EXTRACTION → TRADUCTION → RÉINSERTION

3 outils Python indépendants, chacun avec des garde-fous codifiés en assertions.

## Garde-fous (issus des erreurs commises)

| GF | Erreur d'origine | Protection |
|----|-----------------|------------|
| GF-01 | sed a traduit 30 IDs colonne 1 | Colonnes 0,1,2,3,6 JAMAIS extraites ni touchées |
| GF-02 | sed a mis des accents dans commandes/variables | Colonne script byte-identique, variables $xxx vérifiées |
| GF-03 | Push sans validation directeur | Scripts ne font JAMAIS de git |
| GF-04 | Traduction mot-à-mot | Détection ratio mots identiques > 50% |
| GF-05 | reset --hard sans backup | Backup automatique avant toute écriture |
| GF-06 | CSV parsé avec sed au lieu de csv.reader | csv.reader obligatoire, assertion 7 colonnes |
| GF-07 | Pas de test en jeu avant commit | Checklist finale imprimée obligatoirement |
| GF-08 | Pas d'issues GitHub | Template d'issue généré par le script |
| GF-09 | Agents parallèles sur même fichier | Verrou filelock, 1 processus à la fois |
| GF-10 | Résultat partiel présenté comme complet | Rapport de couverture obligatoire |

## Outil 1 : `tools/extract_rules_text.py`

Lit le CSV, extrait UNIQUEMENT les colonnes text (4) et options (5) → JSON.

```python
COLS_TRADUCTIBLES = frozenset([4, 5])  # text, options
COLS_INTOUCHABLES = frozenset([0, 1, 2, 3, 6])  # id, trigger, conditions, script, notes
```

Sortie : `rules_extract.json` avec pour chaque entrée :
- row_idx, col, text_en, text_fr (null), variables [$xxx], option_id

## Outil 2 : `tools/translate_rules_batch.py`

Applique les traductions dans le JSON. Validations :
- Variables $xxx préservées (GF-02)
- Pas d'accents dans les variables (GF-02c)
- Détection mot-à-mot (GF-04)
- Rapport de couverture (GF-10)

## Outil 3 : `tools/reassemble_rules.py`

Réinjecte les traductions dans le CSV. Validations :
- Backup avant écriture (GF-05)
- IDs byte-identiques (GF-01)
- Script byte-identique (GF-02)
- Nombre de lignes inchangé
- Checklist finale (GF-07)
- Template d'issue (GF-08)

## Options : ne traduire que le label

Format Starsector : `[priority:]optionId:Label visible`
- optionId reste TOUJOURS en anglais
- Seul le label après le dernier `:` est traduit

## Encodage

- Lecture : Latin1 (ISO-8859-1)
- Écriture : Latin1 (ISO-8859-1), newline CRLF
- Apostrophes : U+0027 uniquement, JAMAIS U+2019

## Workflow par bloc

```
1. python tools/extract_rules_text.py --block shrouded --output tmp_batches/extract_shrouded.json
2. [Agent traducteur remplit text_fr dans le JSON]
3. python tools/translate_rules_batch.py --input tmp_batches/extract_shrouded.json --validate
4. python tools/reassemble_rules.py --input tmp_batches/extract_shrouded.json --csv data/campaign/rules.csv
5. [Copier vers mod actif, tester en jeu]
6. [Directeur valide → git add + commit sur dev]
7. [Directeur valide → créer issue GitHub]
```

## Ordre de traduction

| # | Bloc | Segments | Sessions |
|---|------|----------|----------|
| 1 | Shrouded Substrate (L.288-476) | ~30 | 1 |
| 2 | Derelict Vambrace (L.723-970) | ~40 | 1 |
| 3 | Weird Hullmods (L.1409-1870) | ~80 | 2 |
| 4 | AddText épars | ~30 | 0.5 |
| 5 | Bornanow Files (L.9042-13200) | ~500+ | 8-10 |
| **Total** | | **~680+** | **~14** |

## Règles transversales

- UN SEUL agent sur rules.csv à la fois (filelock)
- Marqueurs [FR] intentionnels — ne jamais supprimer
- Pas de push sans validation directeur
- Un bloc = un commit = une issue

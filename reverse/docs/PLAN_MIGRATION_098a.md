# PLAN DE MIGRATION 0.97a vers 0.98a-RC8

## Résumé

3 fichiers BREAKING (colonnes CSV changées), 22 fichiers copie directe, 6 fichiers merge, 4 fichiers merge majeur, 6 fichiers Codex nouveaux.

## Phase 0 : Pré-requis (30 min)
- mod_info.json : gameVersion 0.98a-RC8
- Recompiler JAR Java 17
- Test chargement

## Phase 1 : BREAKING fixes (2h)
- descriptions.csv : nouvelle colonne text5 + 352 nouvelles entrées
- ship_data.csv : 2 nouvelles colonnes + 16 vaisseaux
- market_conditions.csv : nouvelle colonne tags

## Phase 2 : Copies directes (15 min)
22 fichiers identiques 097a/098a

## Phase 3-4 : Merges (6h)
- tips.json, abilities.csv, skill_data.csv, default_ranks.json
- special_items.csv, hull_mods.csv, ship_systems.csv, weapon_data.csv

## Phase 5 : rules.csv (8h+)
41182 lignes vanilla, merge 3-way avec nos 30000 lignes traduites

## Phase 6 : Codex nouveau (4h)
6 fichiers texte a traduire (~260 lignes)

## Phase 7 : Traduction nouveau contenu (20h+)
352 descriptions, ~11000 rules, 95 items/armes/systèmes

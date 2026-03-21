# Changelog

Toutes les modifications notables du mod sont documentees ici.

## [v1.2.10] — 2026-03-21

### Traduction
- 160 strings de dialogue de flotte traduits (postures, combats, poursuites, abordages, tooltips)
- Dialogues de points de saut et de planetes traduits
- Aide campagne traduite (tutoriels, popups, avertissements)
- Tous les marqueurs [FR] retires de strings.json

## [v1.2.9] — 2026-03-21

### Corrections
- 93 variables moteur restaurees ($heOrShe, $hisOrHer, $salvageLeaveText) — les variables traduites par erreur s'affichaient en texte brut en jeu

## [v1.2.8] — 2026-03-21

### Traduction
- rules.csv 100% FR — 3 037 dialogues de campagne (narratif + menus)
- 34 accents corriges dans les dialogues
- 452 IDs corrompus restaures
- Apostrophes typographiques corrigees (U+2019 → U+0027)

### Securite CI/CD
- Check workflow integrity (injection, supply chain, secrets en dur)
- Permissions moindre privilege sur tous les workflows
- Patterns de detection secrets precis (password=, api_key=, cles PEM, tokens)
- Suppression workflows parasites (branch_protection, default_branch)
- Actions mises a jour : checkout@v4, github-script@v7

### Maintenance
- mod_info.json : retrait .skin/.faction/custom_entities du replace
- 75 fichiers obsoletes supprimes
- 8 branches obsoletes supprimees

## [v1.2.7] — 2026-03-20

### Traduction
- 4 933 dialogues campagne traduits
- Scripts contributeur (extract_full.py, assemble.py)

## [v1.2.6] — 2026-03-19

### Traduction
- Labels factions, planetes, grades, types de flottes
- 6 fichiers config JSON traduits

## [v1.2.5] — 2026-03-18

### Traduction
- 10 CSV campagne traduits (marchandises, industries, competences, personnalites, abilities, submarkets, reports, special_items)
- QA ship_names

## [v1.2.4] — 2026-03-18

### Traduction
- strings.json traduit
- Fix apostrophes typographiques

## [v1.2.3] — 2026-03-18

### Corrections
- Fix crash tooltipRefit
- ship_names complet

## [v1.2.2] — 2026-03-17

### Traduction
- descriptions.csv complet
- ship_data.csv, weapon_data.csv, hull_mods.csv

## [v1.2.1] — 2026-03-17

### Corrections
- Fix tips.json
- README update

## [v1.2.0] — 2026-03-17

### Traduction
- Premier pack complet : tips, tooltips, descriptions, ship_names
- 16 missions traduites

---

[Roadmap v1.3+](https://github.com/mipsou/starsector_lang_pack_fr/issues/67)

# Changelog

Toutes les modifications notables du mod sont documentees ici.

## [v1.9.3] — 2026-03-25

### Ajouts / Added
- SalvagePlugin FR : options de salvage traduites (capteurs, balises, relais) via FrenchSalvageInteractionDialogPlugin
- FrenchCampaignPlugin : enregistrement du SalvagePlugin dans le pipeline campagne

### Corrections / Fixed
- descriptions.csv : 3 occurrences "porte-nef" corrigees en "astroporteur" (reservewing, targetingfeed, recalldevice)

### Changements techniques / Technical
- JAR recompile avec 5 classes (FrenchSalvageInteractionDialogPlugin ajoutee)

## [v1.9.2] — 2026-03-24

### Ajouts / Added
- Terminologie : "porte-avions"/"porte-nefs" remplace par "astroporteur" dans tips.json (5), descriptions.csv (18), skill_data.csv (2), tips_translations.csv (5)
- FleetInteractionDialogPlugin : 28 OptionIds traduits (options pre-combat et post-combat en FR)
- getString() override : "Vos forces ont ete" au lieu de "Your forces were"
- advance() polling continu pour traduire les options ajoutees dynamiquement

### Corrections / Fixed
- Crash fix : config null dans le constructeur corrige

### Changements techniques / Technical
- JAR recompile avec Zulu JDK 17
- Accord officiel d'Alex (dev Starsector) obtenu par email

## [v1.2.12] — 2026-03-21

### Traduction
- Guillemets francais « » fonctionnels en jeu (issue #25 resolue — c'etait l'encodage latin-1, pas le moteur)
- tips.json FR restaure (ecran titre)

### Maintenance
- Suppression scripts/, backups/, docs/, tests/, tools/ du repo public
- CI : scan uniquement les lignes ajoutees (faux positifs sur suppressions)

## [v1.2.11] — 2026-03-21

### Corrections
- tips.json restaure depuis git (ecrase par erreur)

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
- Patterns de detection secrets precis (mots de passe, cles API, cles PEM, tokens)
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

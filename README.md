# Starsector Language Pack FR — Repo Dev

![CI](https://github.com/mipsou/starsector_lang_pack_fr_private/actions/workflows/ci.yml/badge.svg?branch=dev)
![Version](https://img.shields.io/github/v/release/mipsou/starsector_lang_pack_fr_private?label=version)
![Starsector](https://img.shields.io/badge/Starsector-0.98a--RC8-orange)

> Dépôt de développement. Le repo public joueur est [starsector_lang_pack_fr](https://github.com/mipsou/starsector_lang_pack_fr).

---

## Architecture

```
data/
├── campaign/           # Dialogues, économie, événements
│   ├── rules.csv       # 4 933 dialogues FR (8 369 lignes CSV)
│   ├── reports.csv     # 330+ événements Intel
│   ├── abilities.csv, commodities.csv, industries.csv, ...
│   ├── batch_*.json    # Textes source EN (102 fichiers)
│   ├── tr_*.json       # Traductions FR (102 fichiers)
│   └── retranslate_batches/  # Retraductions complètes (46 batches)
├── strings/            # Interface, tooltips, tips, ship_names
├── config/             # Labels, planètes, entités, factions
├── characters/         # Compétences, personnalités
├── hullmods/           # Modifications de coque
├── hulls/              # Vaisseaux, variantes .skin
├── weapons/            # Armes
├── shipsystems/        # Systèmes de vaisseaux
├── missions/           # 15 missions traduites
└── world/factions/     # Grades, noms de flottes
```

---

## Pipeline de traduction

1. **Extraction** — `extract_full.py` extrait les textes EN depuis le CSV vanilla
2. **Découpage** — Textes répartis en batches de ~50 (`batch_X_Y.json`)
3. **Traduction** — Agents parallèles produisent les `tr_X_Y.json`
4. **QA multi-passes** — Vérification \n, variables $, terminologie, accents
5. **Assemblage** — `integrate_and_assemble.py` : intègre retranslations → applique sur vanilla → fix accents → fix terminologie
6. **Test en jeu** — Nouvelle partie, vérification dialogues

---

## Fichiers replace (mod_info.json)

| Catégorie | Fichiers | Version |
|-----------|----------|---------|
| Dialogues | rules.csv, reports.csv, strings.json | v1.2.7 |
| Interface | tips.json, tooltips.json, descriptions.csv, ship_names.json | v1.2.0+ |
| Équipement | hull_mods.csv, ship_data.csv, weapon_data.csv, ship_systems.csv | v1.2.2 |
| Campagne | abilities, submarkets, commodities, special_items, industries, market_conditions | v1.2.5 |
| Personnages | skill_data.csv, aptitude_data.csv, personalities.csv | v1.2.5 |
| Config | battle_objectives, contact_tag_data, custom_entities, planets, tag_data | v1.2.6 |
| Factions | default_fleet_type_names, default_ranks | v1.2.6 |
| Missions | mission_list.csv + 15 mission_text.txt | v1.2.7 |

---

## Glossaire terminologique (validé par commission)

| EN | FR | Décision |
|----|-----|----------|
| Hegemony | Hégémonie | Traduction directe |
| Persean League | Ligue Persane | Commission — "Persane" validé, pas "Perséenne" |
| Luddic Church | Église Luddic | Gardé EN — "Luddique" trop proche de "ludique" |
| Luddic Path | Voie de Ludd | Commission |
| Pather | Voiliste | Commission |
| Sindrian Diktat | Diktat Sindrien | Commission |
| Domain | Domaine | Traduction directe |
| Burn bright! | Brûlez bien ! | Commission |

---

## Issues connues

| # | Problème | Cause racine | Statut |
|---|----------|-------------|--------|
| #25 | Guillemets « » non rendus en jeu | Police/moteur Starsector | Ouvert |
| #26 | Variables $shipOrFleet résolues en EN | Code Java hardcodé | Ouvert |
| #27 | UI hardcodée EN (You decide to...) | Code Java non externalisé | Ouvert |

---

## Workflow Git

```
dev → PR → main → sync → public
```

- **dev** : branche de travail (branche par défaut)
- **main** : releases validées uniquement
- **Jamais** de push direct sur main

---

## Notes de version

| Version | Contenu |
|---------|---------|
| v1.2.7 | rules.csv 4 933 dialogues + 15 missions |
| v1.2.6 | Labels, factions, grades, planètes, entités |
| v1.2.5 | 10 CSV campagne/personnages |
| v1.2.4 | strings.json 229 strings |
| v1.2.3 | Fix tooltipRefit, ship_names complet |
| v1.2.2 | 4 CSV équipement |
| v1.2.1 | Fix NNBSP + factions |
| v1.2.0 | Descriptions Codex, variantes .skin |

---

## Licence

EUPL 1.2 — Voir [LICENSE](LICENSE)

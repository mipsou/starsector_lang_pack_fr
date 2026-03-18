# Starsector Language Pack - French

Pack de langue français pour Starsector.

## Statistiques du Projet

### Temps et Activité
[![Temps de Dev](https://img.shields.io/badge/Temps%20de%20Dev-120h-blue)](#)
[![Dernière MàJ](https://img.shields.io/github/last-commit/mipsou/starsector_lang_pack_fr/main?label=Dernière%20MàJ&color=green)](#)
[![Version](https://img.shields.io/github/v/release/mipsou/starsector_lang_pack_fr?label=Version&color=blue)](#)
[![Status](https://img.shields.io/badge/Status-En%20développement-yellow)](#)

### Couverture
[![Fichiers](https://img.shields.io/badge/Fichiers%20Traduits-70%2F1337-blue)](#)
[![Mots](https://img.shields.io/badge/Mots%20Traduits-15k%2F150k-blue)](#)
[![Taille](https://img.shields.io/badge/Taille%20Totale-15%20MB-lightgrey)](#)

### Avancement par fichier

| Fichier | Contenu | Traduit | Vérifié en jeu |
|---------|---------|:-------:|:--------------:|
| `descriptions.csv` | 570 descriptions Codex | ✅ 100% | ✅ |
| `tips.json` | Conseils écran de chargement | ✅ 100% | ✅ |
| `hull_mods.csv` | 120 hullmods (noms + desc) | ✅ 100% | ✅ |
| `ship_data.csv` | Désignations vaisseaux | ✅ 100% | ✅ |
| `ship_systems.csv` | Systèmes de vaisseaux | ✅ 100% | ✅ |
| `weapon_data.csv` | Noms d'armes | ✅ 100% | ✅ |
| `skins/*.skin` | 65 variantes (P, D, XIV, LG…) | ✅ 100% | ✅ |
| `strings.json` | Interface générale | ❌ | ❌ |
| `tooltips.json` | Tooltips interface | ❌ | ❌ |
| `ship_names.json` | Noms de vaisseaux | ❌ | ❌ |

### Qualité
[![Tests](https://img.shields.io/badge/Tests-Passing-success)](#)
[![Couverture](https://img.shields.io/badge/Coverage-75%25-yellowgreen)](#)
[![Issues](https://img.shields.io/github/issues/mipsou/starsector_lang_pack_fr?label=Issues&color=yellow)](#)
[![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen)](#)

## Installation

1. [Téléchargez la dernière version du mod](https://github.com/mipsou/starsector_lang_pack_fr/releases/latest)
2. Extrayez le contenu dans le dossier `mods` de Starsector
3. Activez le mod dans le launcher du jeu

## Structure

```bash
starsector_lang_pack_fr/
├── mod_info.json.........# Configuration du mod
├── data/
│   ├── hullmods/
│   │   └── hull_mods.csv.# 120 hullmods traduits
│   ├── hulls/
│   │   ├── ship_data.csv.# Désignations vaisseaux traduites
│   │   └── skins/........# 65 variantes traduites (P, D, TT, XIV, LG...)
│   ├── shipsystems/
│   │   └── ship_systems.csv # Systèmes de vaisseaux traduits
│   ├── weapons/
│   │   └── weapon_data.csv # Noms d'armes traduits
│   └── strings/..........# Fichiers de traduction
│       ├── descriptions.csv
│       ├── strings.json
│       ├── tips.json
│       ├── tooltips.json
│       └── ship_names.json
└── localization/.........# Source de vérité (fichiers de référence)
    └── data/
        ├── hulls/
        │   └── skins/....# Miroir des variantes traduites
        └── strings/......# Miroir des traductions
```

## Contribution

Pour contribuer à la traduction :
1. Créez un fork du projet
2. Créez une branche pour vos modifications
3. Soumettez une pull request

## Ressources

### Pour les Utilisateurs
- [Forum Starsector](http://fractalsoftworks.com/forum)
- [Wiki Starsector](http://starsector.wikia.com)

### Pour les Développeurs
- [Forum Modding Officiel](https://fractalsoftworks.com/forum/index.php?board=10.0) - Support et discussions
- [Guide de Modding Officiel](https://fractalsoftworks.com/forum/index.php?topic=4760.0) - **LECTURE OBLIGATOIRE**
- [Tutoriel de Modding - Part 1](https://fractalsoftworks.com/forum/index.php?topic=4761.0)
- [Guide de Style](https://fractalsoftworks.com/forum/index.php?topic=7164.0)
- [Guide de Publication](https://fractalsoftworks.com/forum/index.php?topic=15244.0)
- [Documentation du Modding](http://fractalsoftworks.com/docs)
- [Wiki Modding](http://starsector.wikia.com/wiki/Modding)

Pour plus de ressources et de guides, consultez le [devbook.md](devbook.md).

## Licence

Ce mod est sous licence [EUPL 1.2](LICENSE).

## Crédits

- Traduction française par mipsou
- Structure basée sur le mod de traduction chinoise

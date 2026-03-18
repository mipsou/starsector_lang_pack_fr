# Starsector Language Pack - French

![CI](https://github.com/mipsou/starsector_lang_pack_fr/actions/workflows/ci.yml/badge.svg?branch=main)
![Version](https://img.shields.io/github/v/release/mipsou/starsector_lang_pack_fr)
![License](https://img.shields.io/github/license/mipsou/starsector_lang_pack_fr)
![Downloads](https://img.shields.io/github/downloads/mipsou/starsector_lang_pack_fr/total)

## Version 1.2.5

Pack de traduction francaise pour Starsector.

### Liens Rapides
- [Telecharger](https://github.com/mipsou/starsector_lang_pack_fr/releases/latest)
- [Signaler un bug](https://github.com/mipsou/starsector_lang_pack_fr/issues/new)
- [Roadmap & Issues](https://github.com/mipsou/starsector_lang_pack_fr/issues)
- [Forum Starsector](http://fractalsoftworks.com/forum/)

### Fichiers traduits

| Fichier | Contenu | Statut |
|---------|---------|--------|
| `data/strings/tips.json` | Conseils en jeu | OK |
| `data/strings/strings.json` | Dialogues flotte, tutoriels, abordage | OK |
| `data/strings/tooltips.json` | Tooltips flotte (acheter, vendre, saborder...) | OK |
| `data/strings/descriptions.csv` | Descriptions Codex (570 entrees) | OK |
| `data/strings/ship_names.json` | Noms de vaisseaux (2187+ noms, 25 sections) | OK |
| `data/hulls/skins/*.skin` | 65 variantes de vaisseaux (P, D, TT, XIV, LG...) | OK |
| `data/hulls/ship_data.csv` | Designations de vaisseaux (Fregate, Destroyer...) | OK |
| `data/hullmods/hull_mods.csv` | 120 modifications de coque | OK |
| `data/weapons/weapon_data.csv` | Noms d'armes (182 entrees) | OK |
| `data/shipsystems/ship_systems.csv` | Systemes de vaisseaux (59 entrees) | OK |
| `data/campaign/abilities.csv` | 13 capacites de flotte (Transpondeur, Mode Furtif...) | **NEW** |
| `data/campaign/submarkets.csv` | Sous-marches (Marche Ouvert, Marche Noir...) | **NEW** |
| `data/campaign/commodities.csv` | 29 marchandises (Biomasse, Carburant, Noyaux IA...) | **NEW** |
| `data/campaign/special_items.csv` | 30 objets speciaux (Nanoforges, Blueprints...) | **NEW** |
| `data/campaign/industries.csv` | 35 industries de colonies (Mines, Spatioport...) | **NEW** |
| `data/campaign/market_conditions.csv` | 90+ conditions de marche (Biomasse, Monde Aride...) | **NEW** |
| `data/campaign/reports.csv` | 330+ evenements Intel | **NEW** |
| `data/characters/skills/skill_data.csv` | 45+ competences et descriptions lore | **NEW** |
| `data/characters/skills/aptitude_data.csv` | 4 aptitudes (Combat, Commandement...) | **NEW** |
| `data/characters/personalities.csv` | 5 personnalites d'officiers | **NEW** |

### Installation
1. Telechargez la [derniere version](https://github.com/mipsou/starsector_lang_pack_fr/releases/latest)
2. Extrayez l'archive dans le dossier `mods` de Starsector
3. Activez le mod dans le launcher du jeu

### Compatibilite
- Starsector version : 0.97a-RC11
- Mods compatibles : tous (ne modifie que les fichiers de traduction)

### Notes de Version
- v1.2.5 : 10 nouveaux CSV (campagne, competences, personnalites), QA complet ship_names, Biomasse
- v1.2.4 : strings.json traduit (229 strings), correction apostrophes typographiques
- v1.2.3 : Fix crash tooltipRefit, ship_names.json complet (2187+ noms)
- v1.2.2 : Ajout 4 CSV traduits (hullmods, armes, systemes, vaisseaux)
- v1.2.1 : Correction NNBSP + noms de factions en anglais
- v1.2.0 : Descriptions Codex, strings.json, 65 variantes .skin

### Limitations connues
- Certains tooltips d'abilities restent en anglais (texte hardcode dans le moteur Java)
- Le mot "Military" dans les sous-marches est genere par le moteur
- Les titres de missions Intel viennent de rules.csv (30 000+ lignes, prevu futur)
- Les effets mecaniques des competences restent en anglais

### Roadmap
- **v1.2.6** : Labels & entites (types de planetes, entites spatiales, grades, factions)
- **v1.3+** : Override Java pour les textes hardcodes
- **Futur** : rules.csv (dialogues complets)

### Contact
- GitHub : [mipsou/starsector_lang_pack_fr](https://github.com/mipsou/starsector_lang_pack_fr)
- Issues : [Tracker GitHub](https://github.com/mipsou/starsector_lang_pack_fr/issues)

### Licence
EUPL 1.2 - Voir [LICENSE](LICENSE) pour plus de details

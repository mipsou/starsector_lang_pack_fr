# Changelog

## [2.0.0-rc1] - 2026-03-30

### Fixed — Crashes critiques rules.csv
- Suppression du BOM UTF-8 (`\xEF\xBB\xBF`) qui causait `JSONObject["id"] not found` au chargement
- Correction de 7 guillemets surnuméraires causant des cascades Q-state (parser toggle Starsector)
- Suppression d'un guillemet L16521 causant un crash parser
- Remplacement des guillemets typographiques `«»` par `""` dans rules.csv

### Added — Traductions
- Codex traduit EN→FR : Manuel du Spacer (combat, UI, types technologiques)
- ~300 dialogues supplémentaires : gaDHO, Adonya, ElekAlt, PKSentinel, Shrine, Bar, BQFS
- 14 descripteurs de missions EN→FR

### Fixed — Traductions
- Correction de 23× `(lie)` → `(mensonge)` dans rules.csv
- Correction des accents manquants dans 13 fichiers faction
- Correction des textes EN résiduels (Vambrace, GateHauler, flags)

## [2.0.0] - 2026-03-27

### Added
- Migration complète vers Starsector 0.98a-RC8
- 5229 textes traduits EN→FR

## [0.1.0] - 2024-12-30

### Added
- Structure initiale du mod basée sur le mod chinois
- Configuration de base (mod_info.json)
- Fichiers UI de base
- Documentation (README.md, CDC.md)

### Changed
- Mise à jour des informations d'auteur (mipsou)

### Removed
- N/A

## Notes
- Version initiale du mod
- Structure propre pour les futures traductions

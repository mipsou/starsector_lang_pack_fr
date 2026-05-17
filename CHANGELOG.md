# Changelog

## [2.0.4] - 2026-05-17

### Improved — Traductions missions

Retraduction complète des 11 missions via comité pluridisciplinaire (issue #129).
Glossaire factions appliqué systématiquement (Hégémonie, Voie de Ludd, Ligue Persane, Chevaliers de Ludd, Tri-Tachyon).

- `afistfulofcredits` — style noir/western, registre argotique
- `coralnebula` — Ligue Persane, Navarque, Voie de Ludd, force de frappe
- `nothingpersonal` — Académie Galatia, HSS Phoenix, SIGINT Hégémonie
- `direstraits` — blocus Raesvelg, ISS Black Star, Maison Rao, citation
- `thelasthurrah` — arcologies Mayasura, Voie de Ludd, Commodore Jensulte
- `hornetsnest` — Callisto Ibrahim, Disque de Guayota, Dynastie Kanta
- `sinkingthebismarck` — Kane Gleise, Boucher de Troisième Skathi, TTS Chimera
- `forlornhope` — Deuxième Bataille de Chicomoztoc, TTS Invincible, Traité de Crom Cruach
- `thewolfpack` — convoi Gleise, meute Tri-Tachyon, Deimos
- `ambush` — TSM/TRE, classe Doom, Directeur Adjoint de Flotte
- `predatororprey` — TTS Ephemeral, Prédicteur Stratégique, Baikal Daud

## [2.0.0] - 2026-04-01

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
- Correction de 4 articles manquants (du, de la) dans noms Shrouded/Threat

### Migration
- Migration complète vers Starsector 0.98a-RC8
- 5229 textes traduits EN→FR

## [0.1.0] - 2024-12-30

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

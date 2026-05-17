# Changelog

## [2.0.4] - 2026-05-17

### Amélioré — Retraduction complète des missions

Retraduction des 11 missions de combat, dont le texte français était tronqué (ratio < 70% du vanilla). Chaque mission a été retraitée via comité de relecture avec glossaire des factions appliqué systématiquement (Hégémonie, Voie de Ludd, Ligue Persane, Chevaliers de Ludd, Tri-Tachyon).

- *Pour une poignée de crédits* — style noir/western, registre argotique
- *Nébuleuse de Corail* — Ligue Persane, Navarque, Voie de Ludd, force de frappe
- *Rien de personnel* — Académie Galatia, HSS Phoenix, SIGINT Hégémonie
- *Détroit difficile* — blocus Raesvelg, ISS Black Star, Maison Rao, citation
- *Le dernier hourra* — arcologies Mayasura, Voie de Ludd, Commodore Jensulte
- *Le nid de frelons* — Callisto Ibrahim, Disque de Guayota, Dynastie Kanta
- *Couler le Bismarck* — Kane Gleise, Boucher de Troisième Skathi, TTS Chimera
- *Dernier espoir* — Deuxième Bataille de Chicomoztoc, TTS Invincible, Traité de Crom Cruach
- *La meute* — convoi Gleise, meute Tri-Tachyon, Deimos
- *Embuscade* — TSM/TRE, classe Doom, Directeur Adjoint de Flotte
- *Prédateur ou proie* — TTS Ephemeral, Prédicteur Stratégique, Baikal Daud

## [2.0.3] - 2026-05-15

### 🚨 Corrigé — Crash critique avec mods (issue #127)

Suite à un rapport de [@Demotion89](https://github.com/Demotion89) qui rencontrait un crash avec une stack de 25 mods (Nexerelin, Industrial Evolution, Terraforming, etc.), analyse profonde de `rules.csv` :

- **Variable `$hate` corrompue en `$hâte`** (9 occurrences) — variable Java de réputation NPC traduite par erreur par un sed global. Cause probable du crash avec Nexerelin qui manipule cette variable.
- **Variable `$gaDA_rew` tronquée** (3 occurrences) → restaurée en `$gaDA_reward` (missions Galatia Academy)
- **`$fleetOrShip` inventée** (1 occurrence) → corrigée en `$shipOrFleet`
- **`$eOr` et `$eOrE` artefacts** (2 occurrences) → supprimés (étaient des tentatives de gérer l'accord masculin/féminin en français, non supportées par le moteur Starsector)

### Impact joueurs

- Joueurs avec **stack mods + Nexerelin** : fix du crash signalé
- Joueurs **vanilla seul** : pas d'impact visible (les dialogues SDTU/Macario fonctionnent à nouveau correctement)
- Variables d'accord genré (`hisOrHer`, etc.) : 5 cas isolés où la traduction a perdu la dynamique de genre — à traiter en release ultérieure (pas critique)

## [2.0.2] - 2026-04-26

### Corrigé
- Bug CSV : guillemets manquants dans abilities.csv ligne 17 (parsing correct de l'abilité "Générer un Flux Rapide") — merci [@Dorkamrade](https://github.com/Dorkamrade) et [@carlosgmz](https://github.com/carlosgmz)
- Cohérence noms d'abilités dans les rapports tutoriels : "Mode Furtif", "Propulsion d'Urgence", "Salve de Capteurs" alignés avec les noms affichés en jeu (mission Derinkuyu) — merci [@carlosgmz](https://github.com/carlosgmz)
- Tip manquant dans tips.json : "Vous pouvez appuyer sur F2 à tout moment pour ouvrir le Codex"

### Amélioré
- Terminologie sci-fi du tutoriel Derinkuyu : "désengager" (au lieu de "décrocher" trop avionique), "Rendez-vous à Pontus" (destination), "cap sur la ceinture d'astéroïdes" (vecteur navigation)
- CONTRIBUTING.md enrichi : système de confiance contributeur transparent, table contributeurs avec statuts
- CI auto-label : skip propre pour les PRs depuis forks externes

### Communauté
- 🌟 Premier contributeur externe historique : Dorkamrade
- 🟢 Nouveau contributeur 🟢 Confirmé : Ferno (carlosgmz) — fork espagnol en cours

## [2.0.0] - 2026-04-02

### Traduit
- 40 000+ lignes de dialogues, quêtes, événements
- Codex complet (Manuel du Spacer — combat, UI, types technologiques)
- Compétences (40 skills + aptitudes)
- Hullmods (120+), armes (182), systèmes de vaisseaux
- Factions, grades, noms de flottes
- Missions de combat (14)
- Tooltips, tips de chargement, noms de vaisseaux (2187+)
- Marchandises, industries, planètes

### Corrigé
- Crash au chargement corrigé
- Corrections linguistiques (articles, accents, terminologie)

### Compatibilité
- Starsector 0.98a-RC8

## [0.1.0] - 2024-12-30

### Ajouté
- Structure initiale du mod
- Configuration de base

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

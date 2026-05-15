# Changelog

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

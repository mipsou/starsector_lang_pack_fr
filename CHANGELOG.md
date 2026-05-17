# Changelog

## [2.0.5] - 2026-05-17

### Corrigé — Audit textes anglais résiduels (46 manquements)

Passe systématique sur les fichiers de traduction pour débusquer les descriptions encore en anglais.

**`data/strings/descriptions.csv`** — 10 descriptions de systèmes de vaisseaux :
- `combat_burn`, `maneuveringjets`, `plasmajets`, `microburn` — vitesse et maniabilité
- `fortressshield`, `highenergyfocus` — défense et armes énergie
- `phaseteleporter`, `displacer`, `displacer_degraded` — téléportation
- `forgevats_station` — recharge missiles

**`data/weapons/weapon_data.csv`** — 19 descriptions d'armes (2 passes) :
- Passe 1 : SRM DEM Gazer, Répéteur de Choc, Rayon de Faille, Émetteur de Cascade de Faille, Disrupteur de Réalité, Fragment Instable, Décharge Voltaïque, Blaster du Vide, Émanation Hostile + correction typos "Nécessite lhe" → "Nécessite le"
- Passe 2 : phasecl, ionbeam, guardian, tachyonlance, kinetic_fragments, assaying_rift, rift_lightning, abyssal_glare, vortex_launcher

**`data/characters/skills/skill_data.csv`** — 13 descriptions de compétences deprecated :
- Endurance au Combat, Expertise en Armement, Systèmes Défensifs, Contre-Mesures Avancées, Action Évasive, Commandement et Contrôle, Doctrine de Chasseurs, Commandement d'Astroporteurs, Commandant d'Escadrille, Modulation du Réseau Électrique, Conception de Configuration, Logistique de Flotte, Opérations de Récupération

**`data/campaign/reports.csv`** — 4 messages commerce :
- `trade_no_change`, `trade_no_change_negative` — messages journal campagne (lignes commentées, prêtes à l'activation)

### Documenté
- Issue [#129](https://github.com/mipsou/starsector_lang_pack_fr_private/issues/129) : hints tactiques et noms de vaisseaux ennemis hardcodés dans `MissionDefinition.java` — won't fix

---

## [2.0.4] - 2026-05-17

### Amélioré — Retraduction complète des missions

Retraduction des 11 missions de combat via comité pluridisciplinaire (issue #129).
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

---

## [2.0.3] - 2026-05-15

### Corrigé — Crash critique avec mods (issue #127)

- **Variable `$hate` corrompue en `$hâte`** (9 occurrences) — variable Java de réputation NPC
- **Variable `$gaDA_rew` tronquée** (3 occurrences) → restaurée en `$gaDA_reward`
- **`$fleetOrShip` inventée** (1 occurrence) → corrigée en `$shipOrFleet`
- **`$eOr` et `$eOrE` artefacts** (2 occurrences) → supprimés

---

## [2.0.2] - 2026-04-26

### Corrigé
- Bug CSV : guillemets manquants dans abilities.csv ligne 17
- Cohérence noms d'abilités tutoriel Derinkuyu
- Tip manquant dans tips.json

---

## [2.0.0] - 2026-04-02

### Traduit
- 40 000+ lignes de dialogues, quêtes, événements
- Codex complet, compétences, hullmods, armes, systèmes de vaisseaux
- Factions, grades, noms de flottes, missions de combat (14)
- Tooltips, tips, noms de vaisseaux (2187+), marchandises, industries, planètes

### Corrigé
- Crash au chargement (BOM UTF-8, cascades Q-state, guillemets typographiques)

### Compatibilité
- Starsector 0.98a-RC8

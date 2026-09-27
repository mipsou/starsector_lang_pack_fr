# Changelog

## [v2.0.17] - 2026-09-27

> Inclut tout le contenu de la v2.0.16 (jamais publiée seule). QA validée : 3 sessions de jeu consécutives depuis zéro avec Nexerelin 0.12.1e + LazyLib + MagicLib, zéro crash.

### Corrigé

- Armes cachées (variantes de chasseurs, charges utiles, poseurs de mines…) et une modif de coque : leur traduction n'était jamais appliquée (46 armes, dont « Annihilator Rocket Pod (Fighter) »).
- Dialogues : les 6 « Église Luddic » restants deviennent « Église de Ludd », conformément au glossaire.

### Modifié — Traductions de contenu : 6 fichiers ne recopient plus le jeu

- **Armes, compétences, descriptions, conditions de marché, marchandises, industries** : `weapon_data`, `skill_data`, `descriptions`, `market_conditions`, `commodities` et `industries` quittent les chemins du moteur pour `data/i18n/`. Ils ne contiennent plus que l'identifiant et les textes réellement traduits, appliqués par le JAR ; le moteur ne fusionne plus de ligne entière (stats, tags, fabricant) par-dessus le jeu et les autres mods. Aucune cellule traduite perdue (décompte avant/après identique).
- **Descriptions** : un même identifiant peut désigner deux entrées de types différents (ex. `guardian` arme et vaisseau, `nebula` terrain et vaisseau, entités du Codex) ; le JAR les distingue désormais, une traduction n'écrase plus l'autre.
- **Compétences** : les auteurs des citations sont appliqués par le JAR (sans quoi ils repasseraient en anglais).
- Restent livrés comme avant, faute d'accès public dans l'API du jeu : `abilities`, `submarkets`, `aptitude_data`.

## [v2.0.16] - non publiée seule (incluse dans la v2.0.17)

> QA validée : 3 sessions de jeu consécutives depuis zéro avec Nexerelin 0.12.1e + LazyLib + MagicLib, zéro crash (rencontre de flotte, dialogues, marché, Intel).

### Corrigé — Traductions de contenu (vaisseaux, mods de coque, systèmes, objets, planètes, variantes)

Depuis la v2.0.10, une partie des traductions de contenu n'était plus livrée (signalé par Ferno). Pour ces fichiers, le mod ne recopie plus rien du jeu : il ne livre que du texte traduit.

- **Dictionnaires dans `data/i18n/`** : `ship_data`, `hull_mods`, `ship_systems` et `special_items` ne contiennent plus que l'identifiant et les textes traduits. Ils sont lus par le JAR, jamais chargés par le moteur : plus de ligne entière écrasée, donc plus de couleurs ou de valeurs de jeu imposées aux autres mods (#148).
- **Planètes** : `planets.json` ne contient plus que les noms traduits, fusionnés par le moteur (plus aucune couleur, texture ni icône recopiée).
- **Entités de campagne** (relais, balises, caches, épaves, stations…) : leurs noms français sont désormais livrés, par un `custom_entities.json` réduit aux seuls noms et fusionné par le moteur. Jusqu'ici, ce fichier n'était pas livré du tout.
- **Variantes (.skin)** : leur description est traduite par le JAR (`data/i18n/skins.csv`) ; les fichiers `.skin` ne sont plus livrés, ce qui supprime des valeurs de jeu périmées (tags du Codex, points d'équipement, modules intégrés).

### Corrigé — Dialogues de campagne (`rules.csv`)

- Variables restaurées dans 407 textes : grades, noms, récompenses, fusiliers requis, carburant et distance des briefings de l'Académie Galatia, pronoms.
- Variantes de répliques restaurées (salutations par défaut, Imoinu Umbra) et texte parasite `""` retiré.
- Récupération sur les champs de débris : identifiants rétablis.
- 21 dialogues dont les choix pointaient vers de mauvaises suites : identifiants réalignés sur la 0.98a-RC8.
- 137 textes affichés par les scripts de dialogue (messages, infobulles, choix d'histoire) traduits ou corrigés : il en restait en anglais ou à moitié traduits (#165).
- Relecture : élisions et inversions devant les pronoms du jeu (« que $heOrShe », « dit $heOrShe »), terminologie alignée sur le glossaire (Pather, Exécuteur Suprême), contresens corrigés.

### Corrigé — Divers

- « Ouvrir un canal comm » : la ligne rappelant le choix du joueur s'affiche de nouveau (#149).
- Grades et postes : 8 grades manquants ajoutés par Ferno (#147, merci !) puis traduits ; « Gouverneur militaire » ne restait plus en anglais.
- Essaim de défabrication : mise en valeur du texte alignée sur la traduction.
- Descriptions (planètes, factions, vaisseaux) : noms restés en anglais alignés sur le glossaire — Ligue Persane, Église de Ludd, Voie de Ludd, Diktat Sindrien, Chevaliers de Ludd, Domaine, Secteur Persan.
- Accents restaurés : dialogues de rencontre, aide contextuelle, filtres Intel, noms d'entités (« grâce », « à », « écran », « Acceptées »…) et 167 dialogues de campagne écrits sans accents (Chalcedon, Hesperus, Olinadu…).

### Sécurité de publication

- Contrôle automatique « zéro vanilla » (dictionnaires `data/i18n/` et factions) avant chaque publication et dans la CI.
- Une publication est refusée si son tag ne pointe pas sur la version validée.

**Non couvert (à venir)** : autres fichiers encore livrés complets (`weapon_data`, `abilities`, `commodities`…, prévu en v2.0.17), désignations des vaisseaux (« Frigate », « Battleship »… soumises au comité des joueurs), `custom_entities.json`, `channels.json`, `wing_data.csv`, factions `dweller` et `threat`.

---

## [v2.0.15] - 2026-06-10

> Remplace la v2.0.14 (taguée en interne, jamais publiée). QA validée : 3 sessions jeu consécutives depuis zéro avec Nexerelin 0.12.1e + LazyLib + MagicLib, zéro crash.

### Corrigé — Crash au chargement avec Nexerelin (SecurityException)

**Cause racine** : `setFieldByValue()` dans `FrenchLangModPlugin` utilisait `f.getType()` hors du bloc try-catch. Le SecurityManager de Starsector bloque `java.lang.reflect.Field` — la `SecurityException` n'était pas attrapée, crashait `onApplicationLoad()` et empêchait le chargement complet du mod.

**Fix** : `f.getType()` déplacé à l'intérieur du try-catch existant — un seul caractère de décalage, zéro régression fonctionnelle.

### Corrigé — Crash NPE Nexerelin à la création de partie (issue #148)

**Cause racine** : `data/campaign/rules.csv` dans le tableau `replace` désactivait le merge inter-mods des rules. Les rules new-game de Nexerelin (`NGCGetExerelinDefaults`) ne s'exécutaient jamais → `QuestChainSkipEntry.getEntries()` null → NPE fatal dans `ExerelinModPlugin.onNewGame()`. Symptôme visible : les écrans new game Nexerelin (choix de faction, Configure the Sector) n'apparaissaient pas.

**Fix** : `rules.csv` retiré de `replace` — le merge CSV par id conserve les traductions FR des rules vanilla tout en laissant les autres mods injecter leurs propres rules.

Closes #144, closes #148

---

## [v2.0.13] - 2026-05-29

### Maintenance post-v2.0.12

- Nettoyage pipeline release (badge téléchargements, doublon release v2.0.10)
- Restauration release v2.0.10 depuis branche `release/v2.0.10` (ZIP complet avec `pics/`)
- Stabilisation post-hotfix #142 (HJSON comments supprimés, JSON valide)

---

## [v2.0.12] - 2026-05-28

### Corrigé — Compatibilité mods tiers (LunaLib, MagicLib, Tahlan, UAF, Diable Avionics)

**Cause racine** : Starsector charge `strings.json` via `LoadingUtils.loadJSON` — premier mod dans `enabled_mods.json` gagne, aucun merge. Notre mod étant premier, les fichiers strings.json de LunaLib, MagicLib et autres n'étaient jamais lus → `Missing string [saveButtonName]` etc.

**Fix** : `strings.json` est désormais la copie maître incluant toutes les catégories :
- `lunalib` — UI LunaLib (saveButtonName, resetButtonName, header, keybindText…)
- `MagicLib` — bounties, achievements, paintjobs, subsystems…
- `tahlan` — UI Tahlan Shipworks
- `uaf_strings` + `nex_invasion2` — UI UAF
- `diableavionics` — UI Diable Avionics

Note : v2.0.11 (retrait strings.json de `replace`) était un diagnostic erroné — `replace` n'affecte pas ce chemin de code.

---

## [v2.0.11] - 2026-05-28

### Corrigé — Compatibilité LunaLib
- `strings.json` retiré du `replace` → mode merge : les clés UI de LunaLib (saveButtonName, resetButtonName, etc.) ne sont plus écrasées
- Traduction FR conservée intégralement (load order garanti : notre mod charge après vanilla)

### Corrigé — Pipeline release
- `release.sh` step 7 : `git stash push jars/langpack-fr.jar` avant `git checkout main` — évite le crash sur JAR modifié par la compilation

## [v2.0.10] - 2026-05-27

### Ajouté
- Captures d'écran en jeu (`pics/`) : 7 screenshots montrant la traduction FR en action (aptitudes, compétences, dialogue pirate, rencontre combat)
- Pipeline release : `pics/` injecté dans la branche release et le ZIP public
- CI/sécurité : hooks guard-public-repo, allowlist stricte 40 fichiers data/, patch mod_info.json automatique

### Corrigé — Java runtime patches
- Patch runtime via réflexion Java : `abilities`, `submarkets`, `aptitude_data`, `planets` traduits sans crash mods de contenu
- `planets.json` retiré du replace (`PlanetSpec` crash évité)

## [2.0.9] - 2026-05-27

### Corrigé
- Retrait de `planets.json` du tableau replace — crash `PlanetSpec` avec certains mods de contenu

## [2.0.8] - 2026-05-27

### Corrigé — Compatibilité mods de contenu (best effort)
- Retrait de `submarkets.csv`, `abilities.csv`, `aptitude_data.csv` du replace (API sans setter publique → patch runtime à la place)

## [2.0.7] - 2026-05-27

### Ajouté — Patch runtime étendu
- Traduction runtime de `market_conditions`, `commodities`, `industries` via API publique dans `onApplicationLoad()`

## [2.0.6] - 2026-05-26

### Ajouté — Traduction runtime des specs vaisseaux/armes
- Retrait de `ship_data.csv`, `weapon_data.csv`, `hull_mods.csv`, `ship_systems.csv`, `special_items.csv` du tableau replace (conflits mods de contenu)
- `FrenchLangModPlugin` réécrit : méthodes `patchXxx()` via API publique, chargement CSV FR comme dictionnaires, seuls les IDs vanilla patchés

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

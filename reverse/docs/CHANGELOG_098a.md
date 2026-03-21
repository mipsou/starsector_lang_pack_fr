# Starsector 0.98a -- Resume technique pour le mod de traduction FR

Sources :
- [Blog officiel Fractal Softworks](https://fractalsoftworks.com/2025/03/27/starsector-0-98a-release/)
- [Patch notes forum](https://fractalsoftworks.com/forum/index.php?topic=31536.0)
- [Wiki Starsector 0.98a](https://starsector.wiki.gg/wiki/Starsector_0.98a)

Date de sortie : 27 mars 2025

---

## 1. Migration Java 7 vers Java 17

- Le jeu passe de Java 7 a Java 17
- Gain de performance estime a ~30%
- Meilleure stabilite avec un grand nombre de mods
- **Impact traduction** : les fichiers de donnees restent en JSON/CSV, pas de changement d'encodage signale. Le format des fichiers de mod (`mod_info.json`) reste identique.

## 2. Nouveaux fichiers de donnees / formats modifies

### Colonnes CSV ajoutees
- `ship_data.csv` : nouvelle colonne `logistics n/a reason`

### Parametres JSON nouveaux
- `hull_styles.json` : parametre `overloadColor` ajoute
- Fichiers `.wpn` : nouveau champ `fadePreviousFireSound`
- Fichiers `.variant` : champ optionnel `sModdedBuiltIns`
- Fichiers `.system` : support `EmpArcParams`

### settings.json -- nouvelles entrees
- `enableMemoryLeakChecking`
- `enableCampaignMapGridLines`
- `requireTypingDeleteToDeleteSave`
- `allCodexEntriesUnlocked`, `showLockedCodexEntries`
- Configuration autosave (intervalle, activation)
- `weaponSkinsPlayerAndNPC` (skins d'armes par style de coque)

### Support image
- Format `.webp` desormais supporte (avec limitations : pas de glow phase, pas d'animations armes)

### Parametre VM
- `-Dcom.fs.starfarer.launcher_bg=<chemin>` pour personnaliser le fond du launcher

## 3. Nouveau contenu textuel a traduire

### Systeme Codex (refonte complete)
13 categories avec textes a traduire :
- Ships, Stations, Fighters, Weapons, Hullmods, Ship systems
- Special items, Industries, Commodities, Stars & planets
- Planetary conditions, Skills, Abilities, Gallery

Elements UI du Codex :
- Historique de navigation (boutons avant/arriere)
- Barre de recherche (noms d'entrees)
- Bouton "entree aleatoire"
- Navigation par entrees liees
- Info numerique detaillee des systemes de vaisseau
- Info d'utilisation par faction
- Raccourci F2 (ouvre le Codex depuis presque partout, y compris en combat)

### Systeme Intel -- redesign
- Nouveaux tags : New, Important, Story, Fleet log, Exploration
- "Salvor's Tally" : nouvel item intel (entites recuperables par systeme)
- Marqueurs de carte intel : icones personnalisees, noms, points
- Raccourcis clavier : Ctrl+S (sauver tags), Q (restaurer), Shift+Q, 4 (evenements majeurs)

### Sauvegarde/Chargement -- refonte UI
- "Save As" remplace "Save Copy"
- Descriptions personnalisees de sauvegarde
- Fonctionnalite d'autosave (30 min par defaut, rotation 3 slots)
- Recovery automatique de sauvegardes corrompues
- Texte "typing delete to delete save" (confirmation de suppression)

### Recherche de planetes -- refonte
- Filtres par type (etoile/geante gazeuse/planete)
- Filtres : peuplee/revendiquee/libre, exploree/non exploree
- Niveau de danger maximum, emplacements stables minimum
- Ressources requises : minerai, minerai transplutonic, volatils, organique, terres agricoles, ruines
- Compatibilite avec objets de colonie
- Presence d'array solaire orbital, portee hypershunt/cryosleeper

### Simulateur de combat -- refonte
- Options d'officiers/coeurs IA
- Reglages d'agression/comportement
- Qualite des vaisseaux, loadout aleatoire
- Vaisseaux/factions deblocables
- Mode "Stationnaire, defenses seulement"

### Nouvelle condition de colonie
- "Established Polity" (+10% accessibilite, recompense ligue perseenne)

### Nouvelles missions/quetes
- Quete Jethro Bornanew (suite de "Knight Errant")
- Mission d'exploration avec Academicien Cornelius Elek
- Mission bar "Transport VIP en colere"
- Option bourse Academie Galatia (Sebestyen)
- Personnage Tri-Tachyon unique achetant des objets redacted
- Rencontres aux stations frontalieres abandonnees

### Dialogues etendus avec personnages nommes
- Imoinu Kato, Caliban Tseen Ke, Orcus Rao, Rayan Arroyo
- Illustrations uniques de bar pour le Diktat

### Ordres de combat nouveaux
- "Avoid" applicable aux waypoints et objectifs
- "Ignore" : nouvel ordre (le vaisseau ne sera pas poursuivi)

## 4. Changements API affectant le modding

### Nouvelles classes/interfaces
- `CodexEntryPlugin`, `CodexEntryV2`, `CodexDataV2`
- `CoreAutoresolveListener`
- `DetectedEntityListener`
- `TagDisplayAPI`
- `SharedUnlockData`
- `PlanetSearchData`
- `EmpArcParams`

### Nouvelles methodes notables (selection)
**SettingsAPI** : `getAllFactionSpecs()`, `writeJSONToCommon()`, `readJSONFromCommon()`, `getSimOpponents()`, `showCodex()` (3 variantes)

**CombatEngineAPI** : `isInMissionSim()`, `spawnAsteroid()` (6 params)

**FleetMemberAPI** : `getPersonalityOverride()`, `setPersonalityOverride()`

**SectorAPI** : `getCurrentlyOpenMarket()`, `isInSectorGen()`

**TooltipMakerAPI** : `setCodexEntryId()`, `addParaWithMarkup()` (support markup)

**ShipAPI** : `isSpawnDebris()`, `setSpawnDebris()`

### Nouveaux tags
- Systemes de vaisseau : `offensive`, `defensive`, `movement`
- Hullmods/conditions : `hide_in_codex`, `invisible_in_codex`, `codex_require_related`, `codex_unlockable`, `show_in_codex`
- Industries : `do_not_show_in_build_dialog`
- Conditions marche : `planet_search`, `show_in_planet_list`
- Vaisseaux/variantes : `automated`, `MODULE`

### Nouveau systeme de deverrouillage
- `SharedUnlockData` stocke dans `common/core_shared_unlocks.json`
- Persistance inter-sauvegardes

## 5. Nouveau contenu de jeu necessitant traduction

### Nouveau vaisseau
- **Anubis** : croiseur experimental (Tri-Tachyon)
- **Brilliant** : nouvelle variante avec Paladin PD

### Armes modifiees (noms inchanges, stats changees)
Selection des plus impactantes :
- Neoferric Quadcoil, Heavy Adjudicator, Gigacannon
- PD Laser (cout OP reduit, portee augmentee)
- Cryoflamer, Rift Beam, Disintegrator (changements significatifs)
- Shrouded Lens (cout OP fortement reduit)

### Chasseurs modifies
- Piranha, Wasp, Thunder, Trident, Perdition, Spark, Terminator Drone

### Hullmods modifies
- Neural Link : nouvel effet s-mod (transferts instantanes)
- Fabricator Unit : recuperation CR complete apres chaque engagement
- Restriction : hullmods Shrouded et Fragment incompatibles

### Changements de factions
- Mazalot gagne la condition "Luddic Majority"
- Tri-Tachyon devient hostile envers les nouvelles factions redacted
- Flottes de defense systeme ajoutees a : Aztlan, Thule, Hybrasil, Eos Exodus

### Crises de colonie modifiees
- Ligue Perseenne : necessite taille 5 OU 3 colonies dont une taille 4 minimum
- Diktat Sindrien : utilise vaisseaux Lion's Guard
- Defaite Luddic Path : reduit generation d'interet colonie de 50%

### Competences modifiees
- Electronic Warfare, Fighter Uplink, Carrier Group, Hyperspace Topography

## 6. Chargement de mods

- Correction du suivi des numeros de version de mods par sauvegarde
- Stabilite amelioree avec grand nombre de mods (grace a Java 17)
- Indicateur de source du mod dans le Codex (discret)
- Pas de changement fondamental du mecanisme `mod_info.json`

---

## Priorites pour le mod de traduction FR

### Haute priorite (nouveau contenu textuel massif)
1. **Codex** : 13 categories completes avec descriptions, labels, navigation
2. **Intel redesign** : nouveaux tags, Salvor's Tally, marqueurs carte
3. **UI Sauvegarde/Chargement** : tous les nouveaux labels et messages
4. **Recherche planetes** : filtres, labels, conditions
5. **Simulateur combat** : options, labels, modes

### Moyenne priorite (contenu narratif)
6. Quete Jethro Bornanew + mission Cornelius Elek
7. Dialogues etendus (Imoinu Kato, Caliban Tseen Ke, etc.)
8. Mission "Transport VIP en colere"
9. Condition "Established Polity"
10. Rencontres stations frontalieres

### Basse priorite (changements techniques)
11. Nouveaux tags et constantes dans l'API
12. Descriptions modifiees d'armes/hullmods (stats seulement)
13. Nom du vaisseau Anubis + variante Brilliant

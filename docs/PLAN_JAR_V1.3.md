# Plan v1.3 — Override JAR textes hardcodés moteur

## Contexte

Le mod chinois ([TruthOriginem/Starsector-Localization-CN](https://github.com/TruthOriginem/Starsector-Localization-CN)) a résolu le problème des textes hardcodés Java en modifiant directement les JAR du moteur.

Source : `docs/original_manual_processing/original_manual_processing.md`

## Approche chinoise

**Pas un mod** — patch direct qui remplace les fichiers de `starsector-core/` :
- `localization/starfarer.api.jar` — JAR API modifié
- `localization/starfarer_obf.jar` — JAR moteur obfusqué modifié
- `localization/data/` — fichiers data traduits

### Modifications JAR documentées

**1. Constantes UTF-8 partagées** (référencées par d'autres éléments de code) :

| Fichier | Classe | Strings |
|---------|--------|---------|
| starfarer_obf.jar | CharacterStats | "points" |
| starfarer_obf.jar | GLLauncher | "fullscreen", "sound" |
| starfarer_obf.jar | coreui/x | "max" |
| starfarer_obf.jar | ui/newui/X | "next" |
| starfarer.api.jar | FleetGroupIntel | "fleets" |
| starfarer.api.jar | TradeFleetDepartureIntel | "goods", "materiel" |
| starfarer.api.jar | SalvorsTallyIntel | "orbital" |
| starfarer.api.jar | CoreScript | "ships", "cargo", "ships & cargo" |
| starfarer.api.jar | FactionPersonalityPickerPluginImpl | "aggressive", "reckless" |
| starfarer.api.jar | MarketCMD$RaidDangerLevel | "Heavy", "Light", "Moderate", "None", "Minimal", "Extreme" |
| starfarer.api.jar | FactionHostilityIntel | "Hostilities" (tag Intel) |

**2. Logique de code modifiée** :

| # | Problème | Solution |
|---|----------|----------|
| 6 | Troncature texte ship info (Alex coupe 2 derniers chars = ", " anglais) | Adapter la logique de troncature |
| 7 | "Hostilities" hardcodé comme tag Intel | Remplacer le tag string directement |
| 8 | Font combat ship deployment ne s'affiche pas | Changer font vers UI standard, taille 21→14 |
| 9 | Largeur date campagne insuffisante | Élargir à 50px 50px 150px |
| 10 | Format date saves en anglais | Changer locale vers CHINESE (→ FRENCH pour nous) |
| 11 | Largeur colonnes planètes insuffisante | Ajuster les largeurs |

## Plan de workflow v1.3

### Phase 1 — Extraction et analyse
1. Extraire les classes des JAR vanilla avec `jar xf`
2. Décompiler avec [Vineflower](https://github.com/Vineflower/vineflower) ou CFR
3. Identifier TOUS les strings hardcodés visibles en jeu
4. Mapper chaque string → classe Java → méthode

### Phase 2 — Choix d'approche

**Option A — Patch bytecode** (comme le mod chinois) :
- Modifier les constantes UTF-8 dans le bytecode avec ASM ou javassist
- (+) Pas besoin de recompiler, compatible obfuscation
- (-) Casse si Starsector met à jour les classes
- (-) Nécessite remplacement des JAR du jeu (pas un mod propre)

**Option B — Mod Java avec override API** :
- Créer un mod Starsector avec JAR qui utilise `ModPlugin.onApplicationLoad()`
- Patcher les strings au runtime via reflection
- (+) Propre, compatible mods, pas de remplacement de fichiers
- (+) Distribué comme un mod normal (mod_info.json > jars)
- (-) Certains textes non interceptables (launcher, init)
- (-) Plus complexe à implémenter

**Recommandation : Option B d'abord**, fallback Option A pour les textes non interceptables.

### Phase 3 — Implémentation
- Créer `src/` avec classes Java du mod
- `ModPlugin` qui patche les strings au chargement
- Ajouter le JAR compilé au mod via `mod_info.json > jars`
- CI : compilation automatique du JAR

### Phase 4 — Maintenance
- Script de diff automatique quand Starsector se met à jour
- Alerter si une classe modifiée a changé dans la nouvelle version
- Tests de non-régression

## Textes hardcodés identifiés

### Issues liées
- #27 — UI hardcodée (You decide to, Open a comm link, Move in to engage, Your forces, Held in reserve)
- #49 — Filtres Intel (Fleet departures, Gates, Hostilities)
- #50 — Tooltips abilities (Emergency Burn, Sustained Burn)
- #51 — Variable $fleetOrShip
- #52 — Override Java (issue parapluie)

### Textes prioritaires
1. Filtres Intel (visibles en permanence)
2. Tooltips abilities (visibles souvent)
3. Choix narratifs ("You decide to...")
4. Labels combat (Your forces, Held in reserve)
5. Tutoriel

## Références

- [Mod chinois](https://github.com/TruthOriginem/Starsector-Localization-CN)
- [Guide processing JAR](https://github.com/TruthOriginem/Starsector-Localization-CN/blob/master/docs/original_manual_processing/original_manual_processing.md)
- [Starsector modding wiki](https://starsector.wiki.gg/wiki/Getting_started_with_mod_programming)
- [Tutorial translation-friendly mod](https://fractalsoftworks.com/forum/index.php?topic=19405.0)

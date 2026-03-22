# Priorites strings hardcodes — par impact joueur

## Tier 1 — Visible en PERMANENCE (chaque session)

| String EN | String FR | Classe | JAR | Difficulte |
|-----------|-----------|--------|-----|------------|
| "Open a comm link" | "Ouvrir un canal comm" | FleetInteractionDialogPluginImpl | API | Facile |
| "Cut the comm link" | "Couper la comm" | FleetInteractionDialogPluginImpl | API | Facile |
| "Move in to engage" | "Engager le combat" | FleetInteractionDialogPluginImpl | API | Facile |
| "Disengage" | "Rompre le combat" | FleetInteractionDialogPluginImpl | API | Facile |
| "Pursue them" | "Les poursuivre" | FleetInteractionDialogPluginImpl | API | Facile |
| "Your forces" | "Vos forces" | FleetInteractionDialogPluginImpl + ShowDefaultVisual | API | Facile |
| "You decide to..." | "Vous decidez de..." | CargoPods + MarketCMD | API | Facile |

**7 strings, 1 classe principale** — FleetInteractionDialogPluginImpl
C'est le dialogue d'interaction de flotte, vu a CHAQUE rencontre.

## Tier 2 — Visible SOUVENT (tooltips abilities)

| String EN | String FR | Classe | JAR | Difficulte |
|-----------|-----------|--------|-----|------------|
| "Emergency Burn" | "Propulsion d'urgence" | EmergencyBurnAbility | API | Facile |
| "Sustained Burn" | "Propulsion soutenue" | SustainedBurnAbility | API | Facile |
| "Go Dark" | "Mode furtif" | TutorialMissionIntel | API | Facile |
| "Transponder on/off" | "Transpondeur actif/inactif" | TransponderAbility | API | Facile |
| "Interdiction Pulse" | "Impulsion d'interdiction" | InterdictionPulseAbility | API | Facile |

**5 strings** — tooltips des abilities, vus a chaque survol.

## Tier 3 — Visible REGULIEREMENT (Intel, combat)

| String EN | String FR | Classe | JAR | Difficulte |
|-----------|-----------|--------|-----|------------|
| "Hostilities" | "Hostilites" | Tags + FactionHostilityIntel | API | Moyen |
| "Fleet departures" | "Departs de flottes" | Tags + TradeFleetDepartureIntel | API | Moyen |
| "Held in reserve" | "En reserve" | combat/Object/A | OBF | Difficile |
| "ships & cargo" | "vaisseaux et cargaison" | CoreScript | API | Facile |
| "Heavy/Light/Moderate..." | "Lourde/Legere/Moderee..." | MarketCMD$RaidDangerLevel | API | Moyen |

## Tier 4 — Rare (launcher, config)

| String EN | String FR | Classe | JAR | Difficulte |
|-----------|-----------|--------|-----|------------|
| "fullscreen" | - | GLLauncher | OBF | Risque |
| "sound" | - | GLLauncher | OBF | Risque |
| "points" | - | CharacterStats | OBF | Risque |
| "next" | - | ui/newui/X | OBF | Risque |
| "max" | - | coreui/x | OBF | Risque |

**NE PAS TRADUIRE** — ces mots sont aussi des cles de code.
Le mod chinois les note comme "UTF-8 constant shared by code elements".

---

## Strategie recommandee

### Sprint 1 — Quick win (Tier 1 + 2)
12 strings, toutes dans `starfarer.api.jar`, classes lisibles.
Un seul ModPlugin avec reflection peut tout patcher.
**Impact : 90% des textes EN vus en jeu disparaissent.**

### Sprint 2 — Intel + combat (Tier 3)
Tags Intel + niveaux de danger raid.
Necessite de comprendre comment Tags.java est utilise au runtime.

### Sprint 3 — OBF si necessaire (Tier 4)
Seulement si les joueurs le demandent.
Risque de casser des fonctionnalites — les strings OBF Tier 4
sont aussi des identifiants internes.

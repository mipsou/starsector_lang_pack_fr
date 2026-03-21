# Design v1.3 — Java override API publique

## Decision

**API publique uniquement.** Pas de reflection, pas de vmparams, pas de modification des JAR du jeu.

Le sandbox Starsector bloque `java.lang.reflect.Field` dans les scripts de mod. La reflection est interdite.

## Approches evaluees

| Approche | Verdict |
|---|---|
| Reflection (patch static final) | **Bloque** — sandbox interdit java.lang.reflect |
| JAR dans classpath vmparams (SSMSUnlock) | Rejete — manip manuelle joueur |
| Patch JAR vanilla (chinois) | Rejete — modifie les fichiers du jeu |
| **API publique uniquement** | **Retenu** — drop-and-play |

## Architecture

```
mod_info.json
  modPlugin: data.scripts.FrenchLangModPlugin
  jars: [jars/langpack-fr.jar]

FrenchLangModPlugin (BaseModPlugin)
  onGameLoad() → registerPlugin(FrenchCampaignPlugin)

FrenchCampaignPlugin (BaseCampaignPlugin)
  pickInteractionDialogPlugin() → FrenchFleetInteractionDialogPlugin

FrenchFleetInteractionDialogPlugin (extends FleetInteractionDialogPluginImpl)
  init() → translateOptions() + translatePrompt()
  optionSelected() → translateOptions() + translatePrompt()
  translateOptionById() → setOptionText(FR, optionId)
```

## Ce qui est traduit par le JAR

- "Open a comm link" → "Ouvrir un canal comm"
- "Cut the comm link" → "Couper la comm"
- "Move in to engage" → "Engager le combat"
- "Disengage" → "Rompre le combat"
- "Pursue them" → "Les poursuivre"
- "Leave" → "Partir"
- "Continue" → "Continuer"
- "You decide to..." → "Vous decidez de..."

## Ce qui reste en anglais (limitations sandbox)

- Tags Intel (Hostilities, Fleet departures) — static final non patchable
- Your forces / Held in reserve — classes OBF
- You encounter — construit par le moteur
- Admiral skills / Port of origin / Cargo — classes OBF
- Tooltips abilities — a explorer en 0.98a

## Contraintes

- Java 7 bytecode (major version 51) pour JRE 0.97a
- Compilation avec JDK 7 Zulu portable
- Pas de dependance externe
- Compatible tous mods

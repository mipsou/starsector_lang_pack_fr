# Comment Starsector charge un mod Java

## Chaine de chargement

```
1. Joueur lance Starsector
2. Moteur lit mods/enabled_mods.json → liste des mods actives
3. Pour chaque mod active :
   a. Lit mods/<mod>/mod_info.json
   b. Charge les JAR declares dans "jars": ["jars/monmod.jar"]
   c. Instancie la classe declaree dans "modPlugin": "mon.package.MonPlugin"
4. Appelle onApplicationLoad() sur chaque plugin (apres chargement core)
5. Au lancement de partie : appelle onGameLoad() ou onNewGame()
```

## Ce qu'il faut dans mod_info.json

```json
{
  "id": "starsector_lang_pack_fr_dev",
  "name": "Starsector Language Pack - French [DEV]",
  "version": {"major":1, "minor":3, "patch":0},
  "gameVersion": "0.97a-RC11",
  "modPlugin": "data.scripts.FrenchLangModPlugin",
  "jars": ["jars/langpack-fr.jar"],
  "replace": [
    "data/strings/tips.json",
    ...les fichiers existants...
  ]
}
```

### Champs cles :
- **"modPlugin"** : chemin complet de la classe (package.Classe)
  - Doit etendre `com.fs.starfarer.api.BaseModPlugin`
  - Le moteur l'instancie automatiquement
- **"jars"** : liste de JAR a charger dans le classpath
  - Chemin relatif a la racine du mod
  - Le JAR doit contenir la classe du modPlugin

## Structure fichiers du mod

```
starsector_lang_pack_fr/
├── mod_info.json          ← declare jars + modPlugin
├── jars/
│   └── langpack-fr.jar    ← JAR compile
├── src/
│   └── data/
│       └── scripts/
│           └── FrenchLangModPlugin.java  ← source Java
├── data/
│   ├── strings/           ← fichiers texte (replace)
│   ├── campaign/          ← CSV traduits (replace)
│   └── ...
└── ...
```

Note : la convention Starsector pour les sources est `src/` a la racine
du mod. Les .java ne sont PAS charges directement — seul le JAR compile
l'est. Le package doit correspondre au chemin (data.scripts.xxx).

## Le JAR

Le JAR contient les .class compiles :
```
langpack-fr.jar
└── data/
    └── scripts/
        └── FrenchLangModPlugin.class
```

Selon la doc officielle : "If a class exists in both jar and .java file,
the jar version takes precedence."

### Compilation
```bash
# Depuis la racine du mod
javac -cp "../../starsector-core/starfarer.api.jar" \
  -d build/ \
  src/data/scripts/FrenchLangModPlugin.java

# Creer le JAR
jar cf jars/langpack-fr.jar -C build/ .
```

Note : la doc wiki mentionne Java 17 pour le dev mais le JRE du jeu
est Java 7 (0.97a). Verifier la version cible du bytecode.

## Cycle de vie du plugin

```java
public class FrenchLangModPlugin extends BaseModPlugin {

    @Override
    public void onApplicationLoad() throws Exception {
        // Appele UNE FOIS au demarrage, apres chargement core
        // C'est ICI qu'on patche les strings par reflection
        // Le moteur est charge, les classes sont accessibles
    }

    @Override
    public void onGameLoad(boolean newGame) {
        // Appele a chaque chargement de partie
        // Utile pour patcher des choses liees a la campagne
    }
}
```

## Points d'attention

1. **Version Java** — depend de la version du jeu :
   - 0.97a-RC11 = Java 7 (JRE 1.7.0_79) → compiler avec JDK 7
   - 0.98a+ = Java 17 → compiler avec JDK 17
   Notre install est 0.97a. Si on migre vers 0.98a, il faudra
   recompiler le JAR avec JDK 17 et supprimer le JDK 7 portable.
2. **Classpath** — le JAR du mod a acces a starfarer.api.jar
   mais PAS directement a starfarer_obf.jar (il faut reflection)
3. **Ordre de chargement** — les mods sont charges dans un ordre
   non garanti, ne pas dependre d'un autre mod
4. **Pas de remplacement JAR** — on ne touche JAMAIS aux JAR
   du jeu, on patche en memoire au runtime
5. **Convention sources** — sources dans `src/` a la racine du mod,
   package = chemin de classe (ex: data.scripts.FrenchLangModPlugin)
6. **replace** — les fichiers listes dans "replace" de mod_info.json
   empechent le chargement/merge du fichier core correspondant.
   Les graphiques, sons et fichiers Java sont remplaces automatiquement.
7. **modPlugin est un array** — la doc indique JSON Array, mais en
   pratique une string fonctionne aussi (a verifier)
8. **F8 en devmode** — recharge les fichiers data sans redemarrer,
   utile pour tester les traductions

## References (docs officielles)

- [Mod_Info.json Overview](https://starsector.wiki.gg/wiki/Mod_Info.json_Overview) — reference complete des champs
- [Intro to Modding](https://starsector.wiki.gg/wiki/Intro_to_Modding) — guide pas a pas
- [Modding Plugins](https://starsector.wiki.gg/wiki/Modding_Plugins) — lifecycle ModPlugin
- [Getting started with mod programming](https://starsector.wiki.gg/wiki/Getting_started_with_mod_programming) — setup IDE
- [BaseModPlugin API](https://fractalsoftworks.com/starfarer.api/com/fs/starfarer/api/BaseModPlugin.html) — javadoc officielle

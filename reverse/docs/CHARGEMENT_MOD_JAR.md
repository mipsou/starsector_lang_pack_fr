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
│   └── langpack-fr.jar    ← JAR compile (Java 7 bytecode)
├── data/
│   ├── scripts/           ← sources Java (convention, pas charge)
│   │   └── FrenchLangModPlugin.java
│   ├── strings/           ← fichiers texte (replace)
│   ├── campaign/          ← CSV traduits (replace)
│   └── ...
└── ...
```

## Le JAR

Le JAR contient les .class compiles :
```
langpack-fr.jar
└── data/
    └── scripts/
        └── FrenchLangModPlugin.class
```

### Compilation (JDK 7)
```bash
# Depuis la racine du mod
javac -source 1.7 -target 1.7 \
  -cp "../../starsector-core/starfarer.api.jar" \
  -d build/ \
  data/scripts/FrenchLangModPlugin.java

# Creer le JAR
jar cf jars/langpack-fr.jar -C build/ .
```

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

1. **Java 7 obligatoire** — le JRE du jeu est 1.7.0_79
2. **Classpath** — le JAR du mod a acces a starfarer.api.jar
   mais PAS directement a starfarer_obf.jar (il faut reflection)
3. **Ordre de chargement** — les mods sont charges dans un ordre
   non garanti, ne pas dependre d'un autre mod
4. **Pas de remplacement JAR** — on ne touche JAMAIS aux JAR
   du jeu, on patche en memoire au runtime
5. **Convention** — les sources vont dans `data/scripts/` par
   convention Starsector (pas src/)

## References

- [BaseModPlugin API](https://fractalsoftworks.com/starfarer.api/com/fs/starfarer/api/BaseModPlugin.html)
- [Modding Plugins Wiki](https://starsector.fandom.com/wiki/Modding_Plugins)
- [Intro to Modding](https://starsector.fandom.com/wiki/Intro_to_Modding)
- [Exemple MakeAStar](https://github.com/WadeStar/Starsector-Modding-Tutorials)

# Reverse Engineering — Starsector JAR

Espace de travail pour l'analyse des JAR du moteur Starsector.
Objectif : identifier et patcher les textes hardcodés en Java.

## Structure

```
reverse/
├── jars/
│   ├── vanilla/          # Copie des JAR originaux (ne pas modifier)
│   ├── extracted/
│   │   ├── api/          # Classes extraites de starfarer.api.jar
│   │   ├── obf/          # Classes extraites de starfarer_obf.jar
│   │   └── common/       # Classes extraites de fs.common_obf.jar
│   └── .gitkeep
├── decompiled/
│   ├── api/              # Code source decompile (starfarer.api.jar)
│   ├── obf/              # Code source decompile (starfarer_obf.jar)
│   └── common/           # Code source decompile (fs.common_obf.jar)
├── tools/                # Scripts d'extraction et d'analyse
├── strings/
│   ├── hardcoded/        # Strings hardcodes trouves (par classe)
│   └── mapped/           # Mapping string EN → FR avec classe source
├── patches/
│   ├── bytecode/         # Patches ASM/javassist (Option A)
│   └── runtime/          # Code ModPlugin reflection (Option B)
└── docs/                 # Notes d'analyse, screenshots
```

## JAR cibles

| JAR | Taille | Contenu |
|-----|--------|---------|
| `starfarer.api.jar` | API publique | Classes documentees, noms lisibles |
| `starfarer_obf.jar` | Moteur | Classes obfusquees (noms type OOoOOO) |
| `fs.common_obf.jar` | Utilitaires | Classes communes obfusquees |

## Environnement

- **JRE jeu** : Java 7 (1.7.0_79)
- **JDK systeme** : OpenJDK 8 (Temurin 8.0.472)
- **Decompileur** : Vineflower ou CFR (a telecharger dans tools/)
- **Bytecode** : ASM 9.x ou javassist (si Option A)

## Workflow

1. `extract.sh` — Copie et extrait les JAR vanilla
2. `decompile.sh` — Decompile avec Vineflower/CFR
3. `find_strings.sh` — Cherche les strings hardcodes EN
4. Analyse manuelle — Trier les strings traduisibles
5. `map_strings.py` — Generer le mapping EN → FR
6. Implementation — ModPlugin ou bytecode patch

## Regles

- **JAMAIS** modifier les fichiers dans `jars/vanilla/`
- Les JAR vanilla sont dans `.gitignore` (propriete Fractal Softworks)
- Seuls les patches, mappings et scripts sont commites
- Le code decompile n'est PAS commite (copyright)

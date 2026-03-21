# Setup JDK 7 — compatibilite Starsector

## Pourquoi JDK 7 ?

Starsector embarque un JRE 7 (1.7.0_79). Le mod JAR doit etre compile
en bytecode Java 7 pour etre charge par le moteur.

## Options

### Option 1 — JDK 7 natif (recommande)
Telecharger Oracle JDK 7u80 (dernier JDK 7) :
https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html

Ou Zulu JDK 7 (sans compte Oracle) :
https://www.azul.com/downloads/?version=java-7-lts

### Option 2 — Cross-compile depuis JDK 8+
Compiler avec target Java 7 :
```bash
javac -source 1.7 -target 1.7 -bootclasspath $JDK7_HOME/jre/lib/rt.jar ...
```

Avec JDK 8 installe actuellement :
```bash
javac -source 1.7 -target 1.7 -cp "starsector-core/starfarer.api.jar" src/*.java -d build/
```

### Option 3 — Gradle/Maven avec toolchain
```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(7)
    }
}
```

## Verification
```bash
# Verifier le bytecode version d'un .class
javap -verbose MonPlugin.class | grep "major version"
# Java 7 = major version 51
# Java 8 = major version 52
```

## Note
Les outils de decompilation (Vineflower, CFR) peuvent tourner en JDK 8+
sans probleme — ils lisent du bytecode Java 7 et produisent du code source.
Seule la compilation du mod JAR final doit cibler Java 7.

# Examples — minimal language mod plugin

This folder contains a **minimal Java plugin skeleton** for anyone who wants to translate Starsector to another language.

## What it does

Starsector hardcodes some UI strings directly in Java (not in CSV/JSON). To translate them, you need a mod plugin that intercepts and replaces them at runtime.

The example in `src/data/scripts/LangModPlugin.java` shows **one concrete case**: translating the hardcoded dialog prompt `"You decide to..."` to French.

## How to adapt for your language

1. **Change the translation** in `LangModPlugin.java`:
   ```java
   private static final String REPLACEMENT = "Your translation here";
   ```

2. **Rename the class** (e.g. `SpanishLangModPlugin`) to avoid conflicts with other language mods.

3. **Compile to a JAR** targeting Java 7 (Starsector's JRE):
   ```bash
   javac -cp "path/to/starfarer_api.jar" -d build src/data/scripts/*.java
   jar cf jars/yourlang.jar -C build .
   ```

4. **Reference the JAR** in your `mod_info.json`:
   ```json
   "jars": ["jars/yourlang.jar"],
   "modPlugin": "data.scripts.SpanishLangModPlugin"
   ```

## Constraints

- **No reflection** — Starsector's sandbox blocks `java.lang.reflect`.
- **Null-guard everything** — API access can return null during loading/combat screens.
- **Never crash** — always wrap in try/catch with English fallback.

## License

EUPL 1.2 — you can fork and adapt for any language. Keep the EUPL license on your fork (copyleft).

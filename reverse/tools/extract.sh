#!/bin/bash
# Extract Starsector JAR files for analysis
# Usage: ./extract.sh [STARSECTOR_CORE_PATH]

CORE="${1:-D:/Fractal Softworks/Starsector/starsector-core}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$SCRIPT_DIR/.."

echo "=== Extraction JAR Starsector ==="
echo "Source: $CORE"

# 1. Copy vanilla JARs
echo ""
echo "--- Copie JAR vanilla ---"
mkdir -p "$BASE/jars/vanilla"
for jar in starfarer.api.jar starfarer_obf.jar fs.common_obf.jar; do
    if [ -f "$CORE/$jar" ]; then
        cp "$CORE/$jar" "$BASE/jars/vanilla/"
        echo "  OK $jar ($(du -h "$CORE/$jar" | cut -f1))"
    else
        echo "  SKIP $jar (non trouve)"
    fi
done

# 2. Extract classes
echo ""
echo "--- Extraction classes ---"
for name in api obf common; do
    case $name in
        api)    jar="starfarer.api.jar" ;;
        obf)    jar="starfarer_obf.jar" ;;
        common) jar="fs.common_obf.jar" ;;
    esac

    src="$BASE/jars/vanilla/$jar"
    dest="$BASE/jars/extracted/$name"

    if [ -f "$src" ]; then
        rm -rf "$dest"
        mkdir -p "$dest"
        cd "$dest"
        jar xf "$src"
        count=$(find . -name "*.class" | wc -l)
        echo "  OK $jar -> $count classes"
        cd "$BASE"
    fi
done

echo ""
echo "=== Extraction terminee ==="
echo "Prochaine etape: ./decompile.sh"

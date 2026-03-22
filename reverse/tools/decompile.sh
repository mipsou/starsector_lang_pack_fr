#!/bin/bash
# Decompile Starsector JAR files using Vineflower or CFR
# Usage: ./decompile.sh [vineflower|cfr]

DECOMPILER="${1:-vineflower}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$SCRIPT_DIR/.."

echo "=== Decompilation JAR Starsector ==="
echo "Decompileur: $DECOMPILER"

# Check decompiler
VF_JAR="$SCRIPT_DIR/vineflower.jar"
CFR_JAR="$SCRIPT_DIR/cfr.jar"

if [ "$DECOMPILER" = "vineflower" ]; then
    if [ ! -f "$VF_JAR" ]; then
        echo "Vineflower non trouve. Telechargement..."
        echo "  curl -L -o $VF_JAR https://github.com/Vineflower/vineflower/releases/download/1.10.1/vineflower-1.10.1.jar"
        curl -L -o "$VF_JAR" "https://github.com/Vineflower/vineflower/releases/download/1.10.1/vineflower-1.10.1.jar"
    fi
    TOOL_JAR="$VF_JAR"
elif [ "$DECOMPILER" = "cfr" ]; then
    if [ ! -f "$CFR_JAR" ]; then
        echo "CFR non trouve. Telechargement..."
        echo "  curl -L -o $CFR_JAR https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar"
        curl -L -o "$CFR_JAR" "https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar"
    fi
    TOOL_JAR="$CFR_JAR"
else
    echo "Decompileur inconnu: $DECOMPILER (vineflower ou cfr)"
    exit 1
fi

# Decompile each JAR
for name in api obf common; do
    case $name in
        api)    jar="starfarer.api.jar" ;;
        obf)    jar="starfarer_obf.jar" ;;
        common) jar="fs.common_obf.jar" ;;
    esac

    src="$BASE/jars/vanilla/$jar"
    dest="$BASE/decompiled/$name"

    if [ -f "$src" ]; then
        echo ""
        echo "--- Decompilation $jar ---"
        rm -rf "$dest"
        mkdir -p "$dest"

        if [ "$DECOMPILER" = "vineflower" ]; then
            java -jar "$TOOL_JAR" "$src" "$dest"
        else
            # CFR: decompile all classes
            java -jar "$TOOL_JAR" "$src" --outputdir "$dest"
        fi

        count=$(find "$dest" -name "*.java" 2>/dev/null | wc -l)
        echo "  -> $count fichiers .java"
    fi
done

echo ""
echo "=== Decompilation terminee ==="
echo "Prochaine etape: ./find_strings.sh"

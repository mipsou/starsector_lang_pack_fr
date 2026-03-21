#!/bin/bash
# Environnement reverse engineering — JDK 7 local
# Source ce fichier : source tools/env.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# JDK 7 portable (Zulu)
export JAVA7_HOME="$SCRIPT_DIR/jdk7/zulu7.56.0.11-ca-jdk7.0.352-win_x64"
export JAVA_HOME="$JAVA7_HOME"
export PATH="$JAVA7_HOME/bin:$PATH"

# Starsector
export SS_CORE="D:/Fractal Softworks/Starsector/starsector-core"
export SS_API="$SS_CORE/starfarer.api.jar"
export SS_OBF="$SS_CORE/starfarer_obf.jar"

# Reverse workspace
export RE_BASE="$SCRIPT_DIR/.."

echo "JDK 7: $(java -version 2>&1 | head -1)"
echo "SS_CORE: $SS_CORE"
echo "Workspace: $RE_BASE"

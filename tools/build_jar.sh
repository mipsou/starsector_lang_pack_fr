#!/usr/bin/env bash
# =============================================================================
# build_jar.sh — Compile les sources Java et package jars/langpack-fr.jar
#
# Usage :
#   bash tools/build_jar.sh          # build standard
#   bash tools/build_jar.sh clean    # supprime build/ et le JAR
#   bash tools/build_jar.sh check    # verifie les prerequis sans compiler
#
# Prerequis :
#   - JDK 17+ (javac + jar) dans le PATH
#   - starfarer.api.jar dans starsector-core/
#
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Chemins (relatifs a la racine du mod)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOD_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SRC_DIR="$MOD_ROOT/src"
BUILD_DIR="$MOD_ROOT/build"
JAR_DIR="$MOD_ROOT/jars"
JAR_NAME="langpack-fr.jar"
JAR_PATH="$JAR_DIR/$JAR_NAME"

# Starsector core — chemin relatif standard
STARSECTOR_CORE="$MOD_ROOT/../../starsector-core"

# Dependances compile (classpath)
API_JAR="$STARSECTOR_CORE/starfarer.api.jar"
OBF_JAR="$STARSECTOR_CORE/starfarer_obf.jar"
LOG4J_JAR="$STARSECTOR_CORE/log4j-1.2.9.jar"
JSON_JAR="$STARSECTOR_CORE/json.jar"

# Separateur classpath (Windows = ;  Unix = :)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    CP_SEP=";"
else
    CP_SEP=":"
fi

# Java source/target — Java 17 requis (starfarer.api.jar est compile en Java 17)
JAVA_SOURCE="17"
JAVA_TARGET="17"

# JDK 17 embarque dans les worktrees (Zulu JDK 17 portable)
JDK17="$SCRIPT_DIR/../.claude/worktrees/objective-bartik/reverse/tools/jdk17/zulu17.54.21-ca-jdk17.0.13-win_x64/bin"
if [[ -f "$JDK17/javac" || -f "$JDK17/javac.exe" ]]; then
    export PATH="$JDK17:$PATH"
fi

# ---------------------------------------------------------------------------
# Couleurs (si terminal interactif)
# ---------------------------------------------------------------------------
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
die()   { error "$@"; exit 1; }

# ---------------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------------

check_prerequisites() {
    local errors=0

    # javac
    if ! command -v javac &>/dev/null; then
        error "javac introuvable dans le PATH"
        error "  Installer un JDK 17+ (Adoptium, Azul Zulu, Oracle...)"
        ((errors++))
    else
        local jver
        jver=$(javac -version 2>&1 | head -1)
        info "javac : $jver"
    fi

    # jar
    if ! command -v jar &>/dev/null; then
        error "jar introuvable dans le PATH"
        ((errors++))
    fi

    # starfarer.api.jar
    if [[ ! -f "$API_JAR" ]]; then
        error "starfarer.api.jar introuvable : $API_JAR"
        error "  Verifier le chemin vers starsector-core/"
        ((errors++))
    else
        ok "starfarer.api.jar : $API_JAR"
    fi

    # starfarer_obf.jar (requis pour FleetInteractionDialogPluginImpl)
    if [[ ! -f "$OBF_JAR" ]]; then
        error "starfarer_obf.jar introuvable : $OBF_JAR"
        ((errors++))
    else
        ok "starfarer_obf.jar : $OBF_JAR"
    fi

    # log4j (utilise par Logger)
    if [[ ! -f "$LOG4J_JAR" ]]; then
        warn "log4j-1.2.9.jar introuvable : $LOG4J_JAR"
        warn "  La compilation peut echouer sur les imports Logger"
    else
        ok "log4j-1.2.9.jar : $LOG4J_JAR"
    fi

    # Sources
    local java_count
    java_count=$(find "$SRC_DIR" -name '*.java' 2>/dev/null | wc -l)
    if [[ "$java_count" -eq 0 ]]; then
        error "Aucun fichier .java trouve dans $SRC_DIR"
        ((errors++))
    else
        ok "$java_count fichier(s) .java dans src/"
    fi

    return "$errors"
}

do_clean() {
    info "Nettoyage..."
    if [[ -d "$BUILD_DIR" ]]; then
        rm -rf "$BUILD_DIR"
        ok "build/ supprime"
    fi
    if [[ -f "$JAR_PATH" ]]; then
        rm -f "$JAR_PATH"
        ok "$JAR_NAME supprime"
    fi
    ok "Clean termine"
}

do_build() {
    info "=== Build langpack-fr.jar ==="
    info "MOD_ROOT : $MOD_ROOT"
    echo ""

    # Prerequis
    info "Verification des prerequis..."
    if ! check_prerequisites; then
        die "Prerequis manquants — corriger les erreurs ci-dessus"
    fi
    echo ""

    # Lister les sources
    local sources=()
    while IFS= read -r -d '' f; do
        sources+=("$f")
    done < <(find "$SRC_DIR" -name '*.java' -print0)

    info "Sources a compiler :"
    for s in "${sources[@]}"; do
        info "  $(realpath --relative-to="$MOD_ROOT" "$s" 2>/dev/null || echo "$s")"
    done
    echo ""

    # Creer les repertoires
    mkdir -p "$BUILD_DIR"
    mkdir -p "$JAR_DIR"

    # Construire le classpath
    local classpath="${API_JAR}${CP_SEP}${OBF_JAR}${CP_SEP}${LOG4J_JAR}${CP_SEP}${JSON_JAR}"

    # Compiler
    info "Compilation (source=$JAVA_SOURCE, target=$JAVA_TARGET)..."
    javac \
        -source "$JAVA_SOURCE" \
        -target "$JAVA_TARGET" \
        -cp "$classpath" \
        -d "$BUILD_DIR" \
        -encoding UTF-8 \
        -Xlint:none \
        "${sources[@]}"

    local class_count
    class_count=$(find "$BUILD_DIR" -name '*.class' | wc -l)
    ok "Compilation reussie : $class_count classe(s)"
    echo ""

    # Creer le JAR
    info "Packaging $JAR_NAME..."
    jar cf "$JAR_PATH" -C "$BUILD_DIR" .

    local jar_size
    jar_size=$(wc -c < "$JAR_PATH" | tr -d ' ')
    ok "$JAR_NAME cree ($jar_size octets)"
    echo ""

    # Verifier le contenu
    info "Contenu du JAR :"
    jar tf "$JAR_PATH" | grep '\.class$' | while read -r cls; do
        info "  $cls"
    done
    echo ""

    ok "=== Build termine avec succes ==="
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
case "${1:-build}" in
    clean)
        do_clean
        ;;
    check)
        info "=== Verification des prerequis ==="
        if check_prerequisites; then
            echo ""
            ok "Tous les prerequis sont satisfaits"
        else
            echo ""
            die "Prerequis manquants"
        fi
        ;;
    build|"")
        do_build
        ;;
    *)
        echo "Usage: $0 [build|clean|check]"
        exit 1
        ;;
esac

#!/bin/bash
# Find hardcoded English strings in decompiled Starsector code
# Outputs to strings/hardcoded/
# Usage: ./find_strings.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$SCRIPT_DIR/.."

echo "=== Recherche strings hardcodes EN ==="

mkdir -p "$BASE/strings/hardcoded"

# Patterns de textes visibles en jeu (issues #27, #49, #50, #51)
PATTERNS=(
    "You decide to"
    "Open a comm link"
    "Move in to engage"
    "Your forces"
    "Held in reserve"
    "Fleet departures"
    "Hostilities"
    "Emergency Burn"
    "Sustained Burn"
    "Go Dark"
    "Transponder"
    "Sensor Burst"
    "Interdiction Pulse"
    "fleetOrShip"
    "Cut the comm"
    "Leave"
    "Continue"
    "Dismiss"
    "Disengage"
    "Pursue"
    "ships & cargo"
    "Heavy"
    "Light"
    "Moderate"
    "Extreme"
    "Minimal"
    "aggressive"
    "reckless"
    "cautious"
    "steady"
    "timid"
)

for dir in api obf common; do
    src="$BASE/decompiled/$dir"
    out="$BASE/strings/hardcoded/${dir}_strings.txt"

    if [ ! -d "$src" ]; then
        echo "SKIP $dir (non decompile)"
        continue
    fi

    echo ""
    echo "--- Scan $dir ---"
    > "$out"

    for pattern in "${PATTERNS[@]}"; do
        results=$(grep -rn "\"$pattern" "$src" 2>/dev/null)
        if [ -n "$results" ]; then
            echo "## $pattern" >> "$out"
            echo "$results" >> "$out"
            echo "" >> "$out"
            count=$(echo "$results" | wc -l)
            echo "  $pattern : $count occurrences"
        fi
    done

    total=$(grep -c "^##" "$out" 2>/dev/null || echo 0)
    echo "  Total patterns trouves: $total -> $out"
done

echo ""
echo "=== Recherche terminee ==="
echo "Analyser les resultats dans strings/hardcoded/"

#!/usr/bin/env bash
set -e
VERSION="${1:?Usage: ./release.sh <version> [--auto]}"
AUTO=false; [[ "${2:-}" == "--auto" ]] && AUTO=true
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# --- 1. Guard: on dev, clean tree ---
[[ "$(git branch --show-current)" == "dev" ]] || { echo "ERR: not on dev"; exit 1; }
git diff --quiet && git diff --cached --quiet || { echo "ERR: uncommitted changes"; exit 1; }

# --- 2. Forbidden terms ---
FORBIDDEN="porte-nefs|porte-avion|récupérér"
if grep -rIiP "$FORBIDDEN" data/ --include='*.csv' --include='*.json' --include='*.txt' -l; then
  echo "ERR: forbidden terms found"; exit 1
fi

# --- 3. mod_info.json version ---
IFS='.' read -r MAJ MIN PAT <<< "$VERSION"
python3 -c "
import json,sys; m=json.load(open('mod_info.json'))['version']
assert (m['major'],m['minor'],m['patch'])==(${MAJ},${MIN},${PAT}), f'mod_info version mismatch: {m}'
" || { echo "ERR: mod_info.json version != $VERSION"; exit 1; }

# --- 4. Compile JAR ---
JDK="$ROOT/.claude/worktrees/objective-bartik/reverse/tools/jdk17/zulu17.54.21-ca-jdk17.0.13-win_x64/bin"
SS="D:/Fractal Softworks/Starsector/starsector-core"
CP="$SS/starfarer.api.jar;$SS/starfarer_obf.jar;$SS/log4j-1.2.9.jar"
mkdir -p build jars
"$JDK/javac" -source 17 -target 17 -encoding UTF-8 -cp "$CP" -d build src/data/scripts/*.java
"$JDK/jar" cf jars/langpack-fr.jar -C build .
rm -rf build
echo "OK: JAR compiled"

# --- 5. Verify JAR classes ---
EXPECTED="data/scripts/FrenchLangModPlugin data/scripts/FrenchCampaignPlugin data/scripts/FrenchFleetInteractionDialogPlugin data/scripts/FrenchPromptTranslator"
for cls in $EXPECTED; do
  "$JDK/jar" tf jars/langpack-fr.jar | grep -q "${cls}.class" || { echo "ERR: missing $cls"; exit 1; }
done
echo "OK: JAR verified"

# --- 6. PR dev -> main on private ---
git push origin dev
PR_URL=$(gh pr create --repo mipsou/starsector_lang_pack_fr_private \
  --base main --head dev --title "Release v${VERSION}" --body "Release v${VERSION}" 2>/dev/null || \
  gh pr view dev --repo mipsou/starsector_lang_pack_fr_private --json url -q .url)
echo "PR private: $PR_URL"

# --- 7. Merge ---
if $AUTO; then
  gh pr merge --repo mipsou/starsector_lang_pack_fr_private --merge --delete-branch=false
else
  echo "Waiting for merge on private..."; gh pr checks dev --repo mipsou/starsector_lang_pack_fr_private --watch || true
  until gh pr view dev --repo mipsou/starsector_lang_pack_fr_private --json state -q .state | grep -q MERGED; do sleep 10; done
fi
git fetch origin main && git checkout main && git pull origin main

# --- 8. Tag on main ---
git tag -a "v${VERSION}" -m "Release v${VERSION}"
git push origin "v${VERSION}"
git checkout dev

# --- 9. Sync private main -> public dev (force push on public dev only) ---
git push public main:dev --force
echo "OK: public dev synced"

# --- 10. Restore public README ---
git checkout -B public-readme-release public/dev
cp tools/README-public.md README.md
git add README.md && git commit -m "docs: restore public README for v${VERSION}"
git push public public-readme-release:dev --force
git checkout dev

# --- 11. PR dev -> main on public ---
PUB_PR=$(gh pr create --repo mipsou/starsector_lang_pack_fr \
  --base main --head dev --title "Release v${VERSION}" --body "Release v${VERSION}")
echo "PR public: $PUB_PR"

# --- 12. Build ZIP ---
ZIP="starsector-lang-pack-fr-v${VERSION}.zip"
git archive --format=zip --prefix="starsector_lang_pack_fr/" \
  -o "$ZIP" public/dev -- data/ jars/ mod_info.json CHANGELOG.md LICENSE
echo "OK: $ZIP created"

# --- 13. GitHub release ---
gh release create "v${VERSION}" "$ZIP" \
  --repo mipsou/starsector_lang_pack_fr \
  --title "v${VERSION}" --notes "Release v${VERSION}" --latest
echo "DONE: v${VERSION} released"

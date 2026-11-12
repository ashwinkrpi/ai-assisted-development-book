#!/bin/sh
# Copy somaari-common's theme (from its main branch) into this repo. Adapted from somaari-blog.
# The copies are committed, so builds need no network or sibling repo.
# Usage: scripts/sync-common.sh            (somaari-common at $HOME/code/ai-projects/somaari-common)
#        SOMAARI_COMMON=/path scripts/sync-common.sh
#
# Writes:
#   vendor/somaari-common/theme/  theme.js, themes.css, files.json (reference copies)
#   src/assets/fonts/             every fonts/* file in theme/files.json (fonts + OFL licences)
#   src/data/themes.json          theme ids, labels, default and seasonal schedule from theme.js
set -eu

here=$(cd "$(dirname "$0")/.." && pwd)
common=${SOMAARI_COMMON:-"$HOME/code/ai-projects/somaari-common"}

if [ ! -d "$common/.git" ]; then
    echo "error: somaari-common not found at $common (set SOMAARI_COMMON)" >&2
    exit 1
fi
common=$(cd "$common" && pwd)

# Theme: every file listed in theme/files.json, read from main.
if [ -n "$(git -C "$common" status --porcelain -- theme/)" ]; then
    echo "error: $common has uncommitted changes under theme/. Commit them to main first." >&2
    exit 1
fi
list=$(git -C "$common" show main:theme/files.json | sed -n 's/^[[:space:]]*"\([^"]*\)",\{0,1\}[[:space:]]*$/\1/p')
if [ -z "$list" ]; then
    echo "error: no files listed in theme/files.json" >&2
    exit 1
fi

theme="$here/vendor/somaari-common/theme"
fonts="$here/src/assets/fonts"
data="$here/src/data"
rm -rf "$theme.tmp" "$fonts.tmp"
mkdir -p "$theme.tmp" "$fonts.tmp" "$data"
for f in $list; do
    case $f in
        /*|*..*) echo "error: bad path in files.json: $f" >&2; rm -rf "$theme.tmp" "$fonts.tmp"; exit 1 ;;
        fonts/*/*) echo "error: unexpected subfolder in files.json: $f" >&2; rm -rf "$theme.tmp" "$fonts.tmp"; exit 1 ;;
        fonts/*) git -C "$common" show "main:theme/$f" > "$fonts.tmp/${f#fonts/}" ;;
        */*) echo "error: unexpected subfolder in files.json: $f" >&2; rm -rf "$theme.tmp" "$fonts.tmp"; exit 1 ;;
        *) git -C "$common" show "main:theme/$f" > "$theme.tmp/$f" ;;
    esac
done
git -C "$common" show main:theme/files.json > "$theme.tmp/files.json"

# theme.js exports its THEMES, SCHEDULE and DEFAULT_THEME when it finds a CommonJS `module`.
node -e '
const fs = require("fs");
const mod = { exports: {} };
new Function("module", fs.readFileSync(process.argv[1], "utf8"))(mod);
const { THEMES, SCHEDULE, DEFAULT_THEME } = mod.exports;
if (!THEMES || !THEMES[DEFAULT_THEME] || !Array.isArray(SCHEDULE)) {
  console.error("error: theme.js did not export THEMES, SCHEDULE and DEFAULT_THEME");
  process.exit(1);
}
const themes = Object.fromEntries(Object.entries(THEMES).map(([id, t]) => [id, t.label]));
const out = { defaultTheme: DEFAULT_THEME, themes, schedule: SCHEDULE };
fs.writeFileSync(process.argv[2], JSON.stringify(out, null, "\t") + "\n");
' "$theme.tmp/theme.js" "$data/themes.json"

rm -rf "$theme" "$fonts"
mkdir -p "$(dirname "$theme")"
mv "$theme.tmp" "$theme"
mv "$fonts.tmp" "$fonts"
echo "wrote $theme, $fonts and src/data/themes.json ($(echo "$list" | wc -l) theme files, from $(git -C "$common" rev-parse --short main))"

#!/bin/sh
# Copy somaari-common's theme (from its main branch) into this repo, the same way as somaari-blog.
# The copies are committed, so builds need no network or sibling repo. Never edit them by hand.
# Usage: scripts/sync-common.sh            (somaari-common at $HOME/code/ai-projects/somaari-common)
#        SOMAARI_COMMON=/path scripts/sync-common.sh
#
# Writes:
#   public/theme/        every file in theme/files.json (theme.js, themes.css, fonts/ with their
#                        OFL licences), served at /theme/. src/components/Head.astro links
#                        /theme/themes.css, which loads the fonts from /theme/fonts/.
#   src/data/themes.json theme ids, labels, default and seasonal schedule from theme.js, the
#                        somaari-common commit (version) and the default theme's font files to
#                        preload
set -eu

here=$(cd "$(dirname "$0")/.." && pwd)
common=${SOMAARI_COMMON:-"$HOME/code/ai-projects/somaari-common"}

if [ ! -d "$common/.git" ]; then
    echo "error: somaari-common not found at $common (set SOMAARI_COMMON)" >&2
    exit 1
fi
common=$(cd "$common" && pwd)

if [ -n "$(git -C "$common" status --porcelain -- theme/)" ]; then
    echo "error: $common has uncommitted changes under theme/. Commit them to main first." >&2
    exit 1
fi
list=$(git -C "$common" show main:theme/files.json | sed -n 's/^[[:space:]]*"\([^"]*\)",\{0,1\}[[:space:]]*$/\1/p')
if [ -z "$list" ]; then
    echo "error: no files listed in theme/files.json" >&2
    exit 1
fi

theme="$here/public/theme"
mkdir -p "$here/public" "$here/src/data"
rm -rf "$theme.tmp"
mkdir -p "$theme.tmp"
for f in $list; do
    case $f in
        /*|*..*) echo "error: bad path in files.json: $f" >&2; rm -rf "$theme.tmp"; exit 1 ;;
    esac
    mkdir -p "$theme.tmp/$(dirname "$f")"
    git -C "$common" show "main:theme/$f" > "$theme.tmp/$f"
done
git -C "$common" show main:theme/files.json > "$theme.tmp/files.json"
version=$(git -C "$common" rev-parse --short main)

# theme.js exports its THEMES, SCHEDULE and DEFAULT_THEME when it finds a CommonJS `module`. The
# fonts to preload are the @font-face files (Latin subset) of the default theme's --font and
# --font-display families in themes.css.
node -e '
const fs = require("fs");
const [themeJs, themesCss, outFile, version] = process.argv.slice(1);
const mod = { exports: {} };
new Function("module", fs.readFileSync(themeJs, "utf8"))(mod);
const { THEMES, SCHEDULE, DEFAULT_THEME } = mod.exports;
if (!THEMES || !THEMES[DEFAULT_THEME] || !Array.isArray(SCHEDULE)) {
  console.error("error: theme.js did not export THEMES, SCHEDULE and DEFAULT_THEME");
  process.exit(1);
}
const css = fs.readFileSync(themesCss, "utf8");
const block = css.match(new RegExp(":root\\[data-theme=\"" + DEFAULT_THEME + "\"\\][^{]*\\{([^}]*)\\}"));
if (!block) { console.error("error: themes.css has no block for " + DEFAULT_THEME); process.exit(1); }
const first = (name) => { const m = block[1].match(new RegExp("--" + name + ":\\s*([^;]+);")); return m && m[1].trim(); };
const family = (v) => v && (v.startsWith("var(--font)") ? family(first("font")) : v.split(",")[0].trim().replace(/^"|"$/g, ""));
const families = new Set([family(first("font")), family(first("font-display"))]);
const preload = [];
for (const face of css.match(/@font-face\s*\{[^}]*\}/g) || []) {
  const fam = (face.match(/font-family:\s*"?([^";]+)"?;/) || [])[1];
  const src = (face.match(/url\("([^"]+)"\)/) || [])[1];
  const range = (face.match(/unicode-range:\s*([^;]+);/) || [])[1];
  if (families.has(fam) && src && (!range || range.startsWith("U+0000-00FF")) && !preload.includes(src)) preload.push(src);
}
const themes = Object.fromEntries(Object.entries(THEMES).map(([id, t]) => [id, t.label]));
const out = { defaultTheme: DEFAULT_THEME, themes, schedule: SCHEDULE, version, preload };
fs.writeFileSync(outFile, JSON.stringify(out, null, "\t") + "\n");
' "$theme.tmp/theme.js" "$theme.tmp/themes.css" "$here/src/data/themes.json" "$version"

rm -rf "$theme"
mv "$theme.tmp" "$theme"
# Before 2026-11-17 the theme was copied to these; the book now serves public/theme/ instead.
rm -rf "$here/vendor/somaari-common" "$here/src/assets/fonts"
rmdir "$here/vendor" "$here/src/assets" 2>/dev/null || true
echo "wrote $theme and src/data/themes.json ($(echo "$list" | wc -l) theme files, from $version)"

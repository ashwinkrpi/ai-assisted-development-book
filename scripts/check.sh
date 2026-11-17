#!/bin/sh
# The full check: run at the end of the migration (last stage's verify step) and by CI.
# Sub-tasks run only the parts their change touches.
# Checks the chapter code blocks against examples/, runs the script unit tests, builds the site,
# then checks the build against the MkDocs site (paths, heading anchors, no external loads) and
# its site files (robots/sitemap/canonical, CSP inline-script hashes in _headers, Pagefind search).
set -eu
cd "$(dirname "$0")/.."
python3 scripts/check_examples.py
for t in scripts/test_*.py; do
    [ -e "$t" ] && python3 "$t"
done
if [ -f package.json ]; then
    ASTRO_TELEMETRY_DISABLED=1 npm run build --silent
    [ -f scripts/check_site.py ] && python3 scripts/check_site.py
fi
echo "check.sh: all checks passed"

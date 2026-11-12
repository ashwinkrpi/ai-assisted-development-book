#!/bin/sh
# The full check: run at the end of the migration (last stage's verify step) and by CI.
# Sub-tasks run only the parts their change touches.
# Checks the chapter code blocks against examples/, then builds the site.
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

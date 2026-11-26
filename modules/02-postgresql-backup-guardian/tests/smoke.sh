#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash -n guardian.sh install.sh
[[ $(bash guardian.sh --version) == 1.0.0 ]]
bash guardian.sh --help >/dev/null
if bash guardian.sh invalid >/dev/null 2>&1; then exit 1; fi
printf '0\n' | bash guardian.sh interactive >/dev/null
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
for f in database.dump catalogue.txt globals.sql manifest.txt; do echo test > "$tmp/$f"; done
(cd "$tmp"; sha256sum database.dump catalogue.txt globals.sql manifest.txt > SHA256SUMS)
bash guardian.sh verify "$tmp"
echo corruption >> "$tmp/database.dump"
if bash guardian.sh verify "$tmp"; then exit 1; fi
bash guardian.sh list "$tmp"
bash guardian.sh retention-plan "$tmp" 30
[[ -f $tmp/database.dump ]]
echo 'PASS: CLI, menu, intégrité, corruption, simulation.'

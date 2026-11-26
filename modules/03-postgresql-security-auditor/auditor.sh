#!/usr/bin/env bash
# Lanceur portable, sans modification du serveur.
set -euo pipefail
exec python3 "$(dirname "$(readlink -f "$0")")/auditor.py" "$@"

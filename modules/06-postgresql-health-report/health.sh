#!/usr/bin/env bash
# Lanceur sans élévation de privilèges.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if (($# == 0)); then set -- --interactive; fi
exec python3 health.py "$@"

#!/bin/bash
set -euo pipefail
if [ "$#" -eq 0 ]; then set -- interactive; fi
exec python3 "$(dirname "$0")/lab.py" "$@"

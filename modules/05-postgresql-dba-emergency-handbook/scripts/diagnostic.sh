#!/usr/bin/env bash
# Collecte locale en lecture seule ; aucun changement de configuration.
set -euo pipefail
port=${1:-5432}; db=${2:-postgres}
[[ $port =~ ^[0-9]{1,5}$ ]] && ((10#$port >= 1 && 10#$port <= 65535)) || { echo 'Port invalide' >&2; exit 2; }
[[ $db =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]] || { echo 'Nom de base invalide' >&2; exit 2; }
export PGCONNECT_TIMEOUT=5
unset PGSERVICE PGHOSTADDR PGHOST PGPORT PGDATABASE PGOPTIONS PGCLUSTER
printf '=== Système ===\n'; date -u; df -h; df -i; free -h
if command -v pg_lsclusters >/dev/null; then pg_lsclusters; fi
printf '=== PostgreSQL ===\n'
command -v psql >/dev/null || { echo 'Client psql absent' >&2; exit 1; }
timeout 30 psql -X -w -h /var/run/postgresql -p "$port" -d "$db" -v ON_ERROR_STOP=1 -f "$(dirname -- "$0")/diagnostic.sql"

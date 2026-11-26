#!/usr/bin/env bash
# À exécuter uniquement sur un serveur de test jetable.
set -euo pipefail
[[ ${DBA_DISPOSABLE_TEST:-} == YES ]] || { echo 'Instance jetable obligatoire'; exit 1; }
cd "$(dirname "$0")/.."
export PGCONNECT_TIMEOUT=5
lab=$(find modules -maxdepth 1 -name '09-*' -type d)
lib=$(find modules -maxdepth 1 -name '01-*' -type d)
createdb -w -T template0 lab_qa
psql -X -w -v ON_ERROR_STOP=1 -v n=1000 -d lab_qa -f "$lab/sql/00_setup.sql"
[[ $(psql -X -w -At -d lab_qa -c 'select count(*) from dgpc.interventions') == 1000 ]]
while IFS= read -r -d '' f; do echo "SQL: $f"; psql -X -w -v ON_ERROR_STOP=1 -d lab_qa -f "$f"; done < <(find "$lib" -name '*.sql' -print0 | sort -z)
tmp=$(mktemp -d); trap 'rm -rf -- "$tmp"' EXIT
pg_dump -w -Fc -d lab_qa -f "$tmp/test.dump"
createdb -w -T template0 lab_qa_restore
pg_restore -w --exit-on-error --single-transaction --no-owner --no-acl -d lab_qa_restore "$tmp/test.dump"
[[ $(psql -X -w -At -d lab_qa_restore -c 'select count(*) from dgpc.interventions') == 1000 ]]
echo 'Intégration SQL et restauration réussies'

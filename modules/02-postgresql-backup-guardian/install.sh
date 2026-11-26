#!/usr/bin/env bash
# Installation locale, sans activation automatique de tâches.
set -euo pipefail
[[ $EUID == 0 ]] || { echo 'Exécuter avec sudo.'; exit 1; }
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
install -o root -g root -m 0755 guardian.sh /usr/local/sbin/pg-backup-guardian
install -d -o postgres -g postgres -m 0700 /var/lib/postgresql/guardian-backups
echo 'Installation terminée. Voir docs/AUTOMATISATION.md.'

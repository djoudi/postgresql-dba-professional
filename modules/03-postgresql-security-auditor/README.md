# PostgreSQL Security Auditor — Premium 1.0.0
Audit indicatif en lecture seule : 24 contrôles, rapports HTML et JSON privés. Python 3 et client psql requis. Ubuntu/Debian et PostgreSQL 14–18 ciblés, non certifiés.

```bash
sudo -u postgres ./auditor.sh --interactive
./auditor.sh --host /var/run/postgresql --port 5432 --database postgres --output "$HOME/audits"
```
Le dossier doit appartenir au compte exécutant et avoir le mode 0700. Utiliser un compte de supervision dédié en priorité. Voir docs/GUIDE_FR.md pour les limites et les droits. Ne jamais exécuter en root. Aucun changement automatique, aucun secret exporté. Code retour 0 : collecte complète (pas conformité), 1 : échec, 2 : collecte partielle.

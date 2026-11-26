# PostgreSQL DBA Emergency Handbook — Premium

25 runbooks français, PostgreSQL 14–18, Ubuntu/Debian (compatibilité cible). Diagnostic sans modification serveur.

## Démarrage
```bash
bash scripts/diagnostic.sh 5432 postgres
python3 tests/check.py
```
Le script utilise la connexion locale libpq et le compte courant. Authentification préalable requise.

## Index
- [01 — Service indisponible](runbooks/01-service-arrete.md)
- [02 — Connexion TCP refusée](runbooks/02-connexion-refusee.md)
- [03 — Échec de connexion](runbooks/03-authentification.md)
- [04 — Saturation des connexions](runbooks/04-connexions-saturees.md)
- [05 — Disque plein](runbooks/05-disque-plein.md)
- [06 — Croissance WAL](runbooks/06-wal-croissance.md)
- [07 — Corruption suspectée](runbooks/07-corruption.md)
- [08 — Requêtes lentes](runbooks/08-requetes-lentes.md)
- [09 — Blocages](runbooks/09-blocages.md)
- [10 — Deadlocks](runbooks/10-deadlocks.md)
- [11 — Échec de sauvegarde](runbooks/11-backup-echec.md)
- [12 — Échec de restauration](runbooks/12-restore-echec.md)
- [13 — Suppression accidentelle](runbooks/13-suppression.md)
- [14 — CPU élevée](runbooks/14-cpu.md)
- [15 — Pression mémoire / OOM](runbooks/15-memoire.md)
- [16 — Retard de réplication](runbooks/16-replication.md)
- [17 — Archivage WAL en échec](runbooks/17-archivage.md)
- [18 — Autovacuum insuffisant](runbooks/18-autovacuum.md)
- [19 — Risque de wraparound](runbooks/19-wraparound.md)
- [20 — Index suspect ou invalide](runbooks/20-index.md)
- [21 — Échec TLS](runbooks/21-tls.md)
- [22 — Configuration invalide](runbooks/22-configuration.md)
- [23 — Droits insuffisants](runbooks/23-permissions.md)
- [24 — Latence stockage](runbooks/24-io.md)
- [25 — Compromission suspectée](runbooks/25-compromission.md)

Voir [checklists](docs/CHECKLISTS.md) et [reprise](docs/REPRISE.md). Les remédiations sont manuelles et nécessitent autorisation.

# Fiches réflexes DBA

## Connexion et inventaire
```bash
pg_lsclusters
pg_isready -h /var/run/postgresql -p 5432
psql -X -d postgres
```
```sql
SHOW server_version;
SHOW config_file;
SHOW hba_file;
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database WHERE datallowconn;
```
## Sécurité
```sql
SELECT rolname, rolsuper, rolcanlogin FROM pg_roles;
SELECT line_number, auth_method, error FROM pg_hba_file_rules;
SHOW password_encryption;
SHOW ssl;
```
## Performance
```sql
SELECT pid, state, wait_event_type, wait_event FROM pg_stat_activity;
SELECT pid, pg_blocking_pids(pid) FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid))>0;
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum FROM pg_stat_user_tables;
SELECT relname, indexrelname, idx_scan FROM pg_stat_user_indexes;
```
Statistiques cumulatives, droits requis; ne pas supprimer un index sur ce seul critère.
## Sauvegarde (laboratoire)
```bash
umask 077
pg_dump -Fc -d lab_dgpc -f lab.dump
sha256sum lab.dump > lab.dump.sha256
sha256sum -c lab.dump.sha256
pg_restore --list lab.dump
createdb -T template0 lab_restore
pg_restore --exit-on-error --single-transaction --no-owner --no-acl -d lab_restore lab.dump
```
Ne jamais écraser une base existante; vérifier les droits et le contenu après restauration.
## Système et incidents
```bash
df -h
df -i
free -m
ss -lnt
systemctl --failed
journalctl -u postgresql@18-main -n 100 --no-pager
```
Ne jamais supprimer pg_wal. Garder une console indépendante avant modification SSH.
## Réplication
```sql
SELECT pg_is_in_recovery();
SELECT application_name, state, sync_state FROM pg_stat_replication;
SELECT slot_name, active, restart_lsn FROM pg_replication_slots;
```
## Migration
Inventaire → sauvegarde indépendante → arrêt des écritures → export → restauration isolée → contrôles → validation métier → bascule autorisée. Après écritures cible, rollback nécessite réconciliation.

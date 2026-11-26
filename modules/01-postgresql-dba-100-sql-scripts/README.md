# PostgreSQL DBA — 100 scripts SQL

Bibliothèque de diagnostic en français. PostgreSQL 14–18 ciblé. Aucun changement persistant. Les compteurs sont cumulatifs et les résultats dépendent des droits. Ne pas exécuter tous les scripts en boucle sur un serveur chargé.

## Utilisation

```bash
psql -X -h localhost -p 5432 -U dba -d ma_base -v ON_ERROR_STOP=1 -f 01-administration/01_version.sql
```

Utiliser un compte autorisé, sans mot de passe dans la ligne de commande. Les vues privilégiées peuvent échouer; ne pas accorder superuser uniquement pour ces scripts. Les rapports contiennent des métadonnées sensibles.

## Catalogue

| Catégorie | Script | Interprétation |
|---|---|---|
| 01-administration | [01_version](01-administration/01_version.sql) | Identifier la version exacte du serveur. |
| 01-administration | [02_database](01-administration/02_database.sql) | Vérifier le contexte de connexion. |
| 01-administration | [03_databases](01-administration/03_databases.sql) | Repérer les bases accessibles et leurs limites. |
| 01-administration | [04_schemas](01-administration/04_schemas.sql) | Identifier les propriétaires des schémas. |
| 01-administration | [05_extensions](01-administration/05_extensions.sql) | Inventorier les extensions installées. |
| 01-administration | [06_tablespaces](01-administration/06_tablespaces.sql) | Identifier les emplacements externes. |
| 01-administration | [07_tables](01-administration/07_tables.sql) | Inventorier les tables visibles. |
| 01-administration | [08_views](01-administration/08_views.sql) | Inventorier les vues. |
| 01-administration | [09_matviews](01-administration/09_matviews.sql) | Repérer les vues matérialisées non peuplées. |
| 01-administration | [10_sequences](01-administration/10_sequences.sql) | Comparer la valeur connue à la limite. |
| 01-administration | [11_routines](01-administration/11_routines.sql) | Identifier les signatures des routines. |
| 01-administration | [12_triggers](01-administration/12_triggers.sql) | Inventorier les déclencheurs visibles. |
| 01-administration | [13_constraints](01-administration/13_constraints.sql) | Repérer les contraintes non validées. |
| 01-administration | [14_settings](01-administration/14_settings.sql) | Identifier les sources et redémarrages nécessaires. |
| 01-administration | [15_partitions](01-administration/15_partitions.sql) | Examiner les relations parent-enfant, y compris héritage. |
| 02-monitoring | [01_uptime](02-monitoring/01_uptime.sql) | Un démarrage récent peut expliquer des compteurs faibles. |
| 02-monitoring | [02_sessions](02-monitoring/02_sessions.sql) | Comparer les états des connexions. |
| 02-monitoring | [03_connections](02-monitoring/03_connections.sql) | Comparer les clients au plafond, en tenant compte des réserves. |
| 02-monitoring | [04_clients](02-monitoring/04_clients.sql) | Repérer les concentrations de connexions. |
| 02-monitoring | [05_applications](02-monitoring/05_applications.sql) | Identifier les applications dominantes. |
| 02-monitoring | [06_waits](02-monitoring/06_waits.sql) | Une attente idle client est souvent normale. |
| 02-monitoring | [07_database_counters](02-monitoring/07_database_counters.sql) | Comparer des deltas sur un intervalle. |
| 02-monitoring | [08_temp_files](02-monitoring/08_temp_files.sql) | Des deltas élevés signalent des débordements temporaires possibles. |
| 02-monitoring | [09_deadlocks](02-monitoring/09_deadlocks.sql) | Surveiller les nouveaux deadlocks. |
| 02-monitoring | [10_replication](02-monitoring/10_replication.sql) | Les délais NULL ne prouvent pas une panne. |
| 02-monitoring | [11_slots](02-monitoring/11_slots.sql) | Un slot inactif peut retenir du WAL. |
| 02-monitoring | [12_recovery](02-monitoring/12_recovery.sql) | Distinguer primaire et réplique. |
| 02-monitoring | [13_archiver](02-monitoring/13_archiver.sql) | Examiner les échecs récents et la configuration archive. |
| 02-monitoring | [14_wal](02-monitoring/14_wal.sql) | Comparer les compteurs WAL entre deux mesures. |
| 02-monitoring | [15_vacuum_progress](02-monitoring/15_vacuum_progress.sql) | Observer la progression sans interrompre la maintenance. |
| 03-performance | [01_seq_scans](03-performance/01_seq_scans.sql) | Examiner seq_scan avec seq_tup_read; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [02_index_scans](03-performance/02_index_scans.sql) | Examiner idx_scan avec idx_tup_fetch; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [03_inserts](03-performance/03_inserts.sql) | Examiner n_tup_ins avec n_live_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [04_updates](03-performance/04_updates.sql) | Examiner n_tup_upd avec n_tup_hot_upd; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [05_deletes](03-performance/05_deletes.sql) | Examiner n_tup_del avec n_dead_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [06_hot_updates](03-performance/06_hot_updates.sql) | Examiner n_tup_hot_upd avec n_tup_upd; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [07_live_rows](03-performance/07_live_rows.sql) | Examiner n_live_tup avec n_dead_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [08_dead_rows](03-performance/08_dead_rows.sql) | Examiner n_dead_tup avec n_live_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [09_changes_since_analyze](03-performance/09_changes_since_analyze.sql) | Examiner n_mod_since_analyze avec n_live_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [10_insert_since_vacuum](03-performance/10_insert_since_vacuum.sql) | Examiner n_ins_since_vacuum avec n_live_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 03-performance | [11_active_queries](03-performance/11_active_queries.sql) | Identifier les requêtes actives longues sans exposer leur texte. |
| 03-performance | [12_cache_ratio](03-performance/12_cache_ratio.sql) | Le cache OS n’est pas mesuré par ce ratio. |
| 03-performance | [13_table_io](03-performance/13_table_io.sql) | Comparer les lectures sur une période. |
| 03-performance | [14_index_io](03-performance/14_index_io.sql) | Comparer les lectures index sur une période. |
| 03-performance | [15_rollback_ratio](03-performance/15_rollback_ratio.sql) | Un taux élevé peut justifier une analyse applicative. |
| 05-index-statistics | [01_index_usage](05-index-statistics/01_index_usage.sql) | Examiner idx_scan avec idx_tup_read; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 05-index-statistics | [02_index_reads](05-index-statistics/02_index_reads.sql) | Examiner idx_tup_read avec idx_tup_fetch; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 05-index-statistics | [03_index_fetches](05-index-statistics/03_index_fetches.sql) | Examiner idx_tup_fetch avec idx_scan; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 05-index-statistics | [04_invalid_indexes](05-index-statistics/04_invalid_indexes.sql) | Examiner les constructions interrompues ou en cours. |
| 05-index-statistics | [05_index_sizes](05-index-statistics/05_index_sizes.sql) | Les grands index ne sont pas nécessairement inutiles. |
| 05-index-statistics | [06_unused_candidates](05-index-statistics/06_unused_candidates.sql) | Ne jamais supprimer sur ce seul critère. |
| 05-index-statistics | [07_unique_indexes](05-index-statistics/07_unique_indexes.sql) | Identifier les index liés à l’intégrité. |
| 05-index-statistics | [08_partial_indexes](05-index-statistics/08_partial_indexes.sql) | Comparer les prédicats aux requêtes. |
| 05-index-statistics | [09_expression_indexes](05-index-statistics/09_expression_indexes.sql) | Comparer les expressions aux requêtes. |
| 05-index-statistics | [10_column_statistics](05-index-statistics/10_column_statistics.sql) | n_distinct négatif représente une fraction estimée. |
| 08-maintenance | [01_vacuum_count](08-maintenance/01_vacuum_count.sql) | Examiner vacuum_count avec autovacuum_count; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [02_autovacuum_count](08-maintenance/02_autovacuum_count.sql) | Examiner autovacuum_count avec n_dead_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [03_analyze_count](08-maintenance/03_analyze_count.sql) | Examiner analyze_count avec autoanalyze_count; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [04_autoanalyze_count](08-maintenance/04_autoanalyze_count.sql) | Examiner autoanalyze_count avec n_mod_since_analyze; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [05_last_vacuum](08-maintenance/05_last_vacuum.sql) | Examiner last_vacuum avec last_autovacuum; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [06_last_autovacuum](08-maintenance/06_last_autovacuum.sql) | Examiner last_autovacuum avec n_dead_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [07_last_analyze](08-maintenance/07_last_analyze.sql) | Examiner last_analyze avec n_mod_since_analyze; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [08_last_autoanalyze](08-maintenance/08_last_autoanalyze.sql) | Examiner last_autoanalyze avec n_mod_since_analyze; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification. |
| 08-maintenance | [09_database_freeze](08-maintenance/09_database_freeze.sql) | Comparer à autovacuum_freeze_max_age; ne pas attendre le wraparound. |
| 08-maintenance | [10_table_freeze](08-maintenance/10_table_freeze.sql) | Identifier les relations à surveiller pour le gel des XID. |
| 04-security | [01_superusers](04-security/01_superusers.sql) | Vérifier la nécessité de chaque superutilisateur. |
| 04-security | [02_login_roles](04-security/02_login_roles.sql) | Contrôler les comptes de connexion. |
| 04-security | [03_create_roles](04-security/03_create_roles.sql) | Examiner les délégations de gestion des rôles. |
| 04-security | [04_create_db](04-security/04_create_db.sql) | Examiner les droits de création de bases. |
| 04-security | [05_replication_roles](04-security/05_replication_roles.sql) | Limiter les comptes de réplication. |
| 04-security | [06_bypass_rls](04-security/06_bypass_rls.sql) | Vérifier les exceptions RLS. |
| 04-security | [07_memberships](04-security/07_memberships.sql) | Examiner les appartenances et délégations. |
| 04-security | [08_hba_errors](04-security/08_hba_errors.sql) | Vue privilégiée; aucune ligne ne garantit pas une politique sûre. |
| 04-security | [09_hba_trust](04-security/09_hba_trust.sql) | Examiner chaque règle trust; vue privilégiée. |
| 04-security | [10_hba_methods](04-security/10_hba_methods.sql) | Examiner l’ordre des règles; vue privilégiée. |
| 04-security | [11_tls_sessions](04-security/11_tls_sessions.sql) | Les sockets locaux ne nécessitent pas TLS. |
| 04-security | [12_security_settings](04-security/12_security_settings.sql) | Comparer aux exigences locales; password_encryption ne prouve pas le format des anciens secrets. |
| 04-security | [13_public_grants](04-security/13_public_grants.sql) | Inventaire limité aux droits visibles. |
| 04-security | [14_definer_functions](04-security/14_definer_functions.sql) | Examiner propriétaire, search_path et droits EXECUTE. |
| 04-security | [15_rls_tables](04-security/15_rls_tables.sql) | Vérifier les tables nécessitant une isolation par ligne. |
| 06-storage | [01_database_sizes](06-storage/01_database_sizes.sql) | Comparer les tailles dans le temps. |
| 06-storage | [02_total_table_sizes](06-storage/02_total_table_sizes.sql) | Inclut index et TOAST. |
| 06-storage | [03_heap_sizes](06-storage/03_heap_sizes.sql) | Taille du fork principal uniquement. |
| 06-storage | [04_table_sizes](06-storage/04_table_sizes.sql) | Inclut TOAST mais pas les index principaux. |
| 06-storage | [05_index_total](06-storage/05_index_total.sql) | Comparer le poids des index. |
| 06-storage | [06_toast_sizes](06-storage/06_toast_sizes.sql) | Repérer les valeurs volumineuses. |
| 06-storage | [07_schema_sizes](06-storage/07_schema_sizes.sql) | Somme des tables physiques utilisateur. |
| 06-storage | [08_tablespace_sizes](06-storage/08_tablespace_sizes.sql) | Peut nécessiter des droits élevés et des accès disque. |
| 06-storage | [09_wal_directory](06-storage/09_wal_directory.sql) | Vue privilégiée; ne jamais supprimer manuellement le WAL. |
| 06-storage | [10_sequence_capacity](06-storage/10_sequence_capacity.sql) | Tenir compte du sens, du cache et du cycle. |
| 07-locks-transactions | [01_blocked](07-locks-transactions/01_blocked.sql) | Identifier les bloqueurs sans terminer de session. |
| 07-locks-transactions | [02_lock_modes](07-locks-transactions/02_lock_modes.sql) | Comparer les modes et les attentes. |
| 07-locks-transactions | [03_waiting_locks](07-locks-transactions/03_waiting_locks.sql) | Identifier les attentes en cours. |
| 07-locks-transactions | [04_relation_locks](07-locks-transactions/04_relation_locks.sql) | Examiner les verrous de la base courante. |
| 07-locks-transactions | [05_long_transactions](07-locks-transactions/05_long_transactions.sql) | Une transaction longue peut retenir des versions de lignes. |
| 07-locks-transactions | [06_idle_transactions](07-locks-transactions/06_idle_transactions.sql) | Examiner les transactions oubliées. |
| 07-locks-transactions | [07_prepared_transactions](07-locks-transactions/07_prepared_transactions.sql) | Ne pas résoudre sans connaître le coordinateur. |
| 07-locks-transactions | [08_advisory_locks](07-locks-transactions/08_advisory_locks.sql) | Identifier les verrous applicatifs. |
| 07-locks-transactions | [09_xmin](07-locks-transactions/09_xmin.sql) | Identifier les horizons de visibilité anciens. |
| 07-locks-transactions | [10_timeouts](07-locks-transactions/10_timeouts.sql) | Comparer les délais aux besoins applicatifs. |

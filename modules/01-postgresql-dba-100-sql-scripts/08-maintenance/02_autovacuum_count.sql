-- Objectif : autovacuum count
-- Interprétation : Examiner autovacuum_count avec n_dead_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT schemaname,relname,autovacuum_count,n_dead_tup FROM pg_stat_user_tables ORDER BY autovacuum_count DESC NULLS LAST LIMIT 100;
ROLLBACK;

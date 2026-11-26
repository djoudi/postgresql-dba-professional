-- Objectif : index io
-- Interprétation : Comparer les lectures index sur une période.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT schemaname,relname,idx_blks_read,idx_blks_hit FROM pg_statio_user_tables ORDER BY idx_blks_read DESC NULLS LAST LIMIT 100;
ROLLBACK;

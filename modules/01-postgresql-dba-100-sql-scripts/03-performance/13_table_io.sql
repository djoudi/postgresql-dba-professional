-- Objectif : table io
-- Interprétation : Comparer les lectures sur une période.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT schemaname,relname,heap_blks_read,heap_blks_hit FROM pg_statio_user_tables ORDER BY heap_blks_read DESC LIMIT 100;
ROLLBACK;

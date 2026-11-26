-- Objectif : waits
-- Interprétation : Une attente idle client est souvent normale.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT wait_event_type,wait_event,count(*) FROM pg_stat_activity WHERE wait_event IS NOT NULL GROUP BY 1,2 ORDER BY 3 DESC;
ROLLBACK;

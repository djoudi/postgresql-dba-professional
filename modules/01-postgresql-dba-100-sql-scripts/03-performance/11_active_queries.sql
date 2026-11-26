-- Objectif : active queries
-- Interprétation : Identifier les requêtes actives longues sans exposer leur texte.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT pid,now()-query_start AS duration,wait_event_type FROM pg_stat_activity WHERE state='active' AND pid<>pg_backend_pid() ORDER BY duration DESC;
ROLLBACK;

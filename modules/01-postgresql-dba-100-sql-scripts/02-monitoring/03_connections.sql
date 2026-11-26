-- Objectif : connections
-- Interprétation : Comparer les clients au plafond, en tenant compte des réserves.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT count(*) FILTER (WHERE backend_type='client backend') AS clients,current_setting('max_connections') AS maximum FROM pg_stat_activity;
ROLLBACK;

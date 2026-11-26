-- Objectif : cache ratio
-- Interprétation : Le cache OS n’est pas mesuré par ce ratio.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT datname,round(100.0*blks_hit/NULLIF(blks_hit+blks_read,0),2) AS hit_pct FROM pg_stat_database;
ROLLBACK;

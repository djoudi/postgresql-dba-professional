-- Objectif : rollback ratio
-- Interprétation : Un taux élevé peut justifier une analyse applicative.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT datname,round(100.0*xact_rollback/NULLIF(xact_commit+xact_rollback,0),2) FROM pg_stat_database;
ROLLBACK;

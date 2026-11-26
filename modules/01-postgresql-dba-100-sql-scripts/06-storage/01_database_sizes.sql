-- Objectif : database sizes
-- Interprétation : Comparer les tailles dans le temps.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT datname,pg_database_size(oid) AS bytes FROM pg_database WHERE has_database_privilege(oid,'CONNECT') ORDER BY bytes DESC;
ROLLBACK;

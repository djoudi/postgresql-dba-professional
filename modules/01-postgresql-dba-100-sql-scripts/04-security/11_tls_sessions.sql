-- Objectif : tls sessions
-- Interprétation : Les sockets locaux ne nécessitent pas TLS.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT a.datname,a.usename,s.ssl,s.version,s.cipher FROM pg_stat_ssl s JOIN pg_stat_activity a USING(pid);
ROLLBACK;

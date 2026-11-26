-- Objectif : routines
-- Interprétation : Identifier les signatures des routines.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT n.nspname, p.proname, p.prokind, pg_get_function_identity_arguments(p.oid) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema');
ROLLBACK;

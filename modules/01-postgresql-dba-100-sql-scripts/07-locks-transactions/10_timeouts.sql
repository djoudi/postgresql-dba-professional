-- Objectif : timeouts
-- Interprétation : Comparer les délais aux besoins applicatifs.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT name,setting,unit FROM pg_settings WHERE name IN ('lock_timeout','statement_timeout','idle_in_transaction_session_timeout','deadlock_timeout');
ROLLBACK;

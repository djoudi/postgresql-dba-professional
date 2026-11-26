-- Objectif : replication
-- Interprétation : Les délais NULL ne prouvent pas une panne.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT application_name,state,sync_state,write_lag,flush_lag,replay_lag FROM pg_stat_replication;
ROLLBACK;

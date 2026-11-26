-- Objectif : archiver
-- Interprétation : Examiner les échecs récents et la configuration archive.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT archived_count,failed_count,last_archived_time,last_failed_time,stats_reset FROM pg_stat_archiver;
ROLLBACK;

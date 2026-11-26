-- Objectif : vacuum progress
-- Interprétation : Observer la progression sans interrompre la maintenance.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT pid,datname,relid::regclass,phase,heap_blks_total,heap_blks_scanned FROM pg_stat_progress_vacuum WHERE datname=current_database();
ROLLBACK;

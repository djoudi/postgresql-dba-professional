-- Objectif : temp files
-- Interprétation : Des deltas élevés signalent des débordements temporaires possibles.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT datname,temp_files,temp_bytes FROM pg_stat_database ORDER BY temp_bytes DESC;
ROLLBACK;

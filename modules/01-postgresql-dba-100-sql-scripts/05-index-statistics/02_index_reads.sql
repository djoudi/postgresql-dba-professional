-- Objectif : index reads
-- Interprétation : Examiner idx_tup_read avec idx_tup_fetch; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT schemaname,relname,indexrelname,idx_tup_read,idx_tup_fetch FROM pg_stat_user_indexes ORDER BY idx_tup_read DESC NULLS LAST LIMIT 100;
ROLLBACK;

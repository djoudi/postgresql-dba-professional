-- Objectif : insert since vacuum
-- Interprétation : Examiner n_ins_since_vacuum avec n_live_tup; tenir compte de la période de collecte et du volume. Un classement ne constitue pas une recommandation de modification.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT schemaname,relname,n_ins_since_vacuum,n_live_tup FROM pg_stat_user_tables ORDER BY n_ins_since_vacuum DESC NULLS LAST LIMIT 100;
ROLLBACK;

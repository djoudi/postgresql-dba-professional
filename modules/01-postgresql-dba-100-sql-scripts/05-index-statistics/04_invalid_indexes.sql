-- Objectif : invalid indexes
-- Interprétation : Examiner les constructions interrompues ou en cours.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT indexrelid::regclass,indisvalid,indisready FROM pg_index WHERE NOT indisvalid OR NOT indisready;
ROLLBACK;

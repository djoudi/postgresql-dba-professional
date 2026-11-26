-- Objectif : hba errors
-- Interprétation : Vue privilégiée; aucune ligne ne garantit pas une politique sûre.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT line_number,error FROM pg_hba_file_rules WHERE error IS NOT NULL;
ROLLBACK;

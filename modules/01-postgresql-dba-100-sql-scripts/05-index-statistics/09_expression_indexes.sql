-- Objectif : expression indexes
-- Interprétation : Comparer les expressions aux requêtes.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT indexrelid::regclass,pg_get_expr(indexprs,indrelid) FROM pg_index WHERE indexprs IS NOT NULL;
ROLLBACK;

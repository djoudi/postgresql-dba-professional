-- Objectif : toast sizes
-- Interprétation : Repérer les valeurs volumineuses.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT oid::regclass,pg_total_relation_size(reltoastrelid) AS bytes FROM pg_class WHERE reltoastrelid<>0 ORDER BY bytes DESC;
ROLLBACK;

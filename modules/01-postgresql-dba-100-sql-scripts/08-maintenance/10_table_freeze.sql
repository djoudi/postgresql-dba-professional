-- Objectif : table freeze
-- Interprétation : Identifier les relations à surveiller pour le gel des XID.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT oid::regclass,age(relfrozenxid) AS xid_age FROM pg_class WHERE relkind IN ('r','m','t') ORDER BY xid_age DESC LIMIT 100;
ROLLBACK;

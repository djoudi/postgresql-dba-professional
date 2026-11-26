-- Objectif : xmin
-- Interprétation : Identifier les horizons de visibilité anciens.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT pid,backend_xmin,age(backend_xmin) AS xid_age FROM pg_stat_activity WHERE backend_xmin IS NOT NULL ORDER BY xid_age DESC;
ROLLBACK;

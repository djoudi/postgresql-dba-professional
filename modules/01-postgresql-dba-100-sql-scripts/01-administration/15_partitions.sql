-- Objectif : partitions
-- Interprétation : Examiner les relations parent-enfant, y compris héritage.
-- Droits : connexion à la base; pg_read_all_stats/pg_monitor ou droits spécifiques selon la vue.
-- PostgreSQL 14–18 ciblé. Exécution avec psql -X -v ON_ERROR_STOP=1 -f fichier.sql
-- Attention : résultats potentiellement sensibles; coût variable selon le serveur.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '3s';
SELECT inhparent::regclass AS parent, inhrelid::regclass AS child FROM pg_inherits;
ROLLBACK;

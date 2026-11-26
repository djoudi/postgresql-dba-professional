\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
BEGIN;
UPDATE dgpc.interventions SET response_minutes=20 WHERE id=1;
SAVEPOINT s;
UPDATE dgpc.interventions SET response_minutes=30 WHERE id=1;
ROLLBACK TO s;
SELECT response_minutes FROM dgpc.interventions WHERE id=1;
ROLLBACK;

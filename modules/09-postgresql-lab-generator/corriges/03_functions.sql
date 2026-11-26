\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
BEGIN;
CREATE FUNCTION dgpc.open_count(p_unit int) RETURNS bigint LANGUAGE sql STABLE AS $$ SELECT count(*) FROM dgpc.interventions WHERE unit_id=p_unit AND status='open' $$;
SELECT dgpc.open_count(42);
ROLLBACK;

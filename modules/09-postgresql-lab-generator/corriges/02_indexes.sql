\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM dgpc.interventions WHERE unit_id=42 AND status='open';
BEGIN;
CREATE INDEX lab_open_idx ON dgpc.interventions(unit_id) WHERE status='open';
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM dgpc.interventions WHERE unit_id=42 AND status='open';
ROLLBACK;

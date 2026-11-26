\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
BEGIN;
CREATE PROCEDURE dgpc.close_case(p_id bigint) LANGUAGE plpgsql AS $$ BEGIN UPDATE dgpc.interventions SET status='closed' WHERE id=p_id AND status='open'; IF NOT FOUND THEN RAISE EXCEPTION 'Intervention absente ou clôturée'; END IF; END $$;
CALL dgpc.close_case(7);
SELECT status FROM dgpc.interventions WHERE id=7;
ROLLBACK;

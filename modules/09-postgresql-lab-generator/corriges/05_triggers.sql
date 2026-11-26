\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
BEGIN;
CREATE TABLE dgpc.audit(id bigint, old_status text,new_status text, changed_at timestamptz DEFAULT clock_timestamp());
CREATE FUNCTION dgpc.audit_fn() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN INSERT INTO dgpc.audit(id,old_status,new_status) VALUES(NEW.id,OLD.status,NEW.status); RETURN NEW; END $$;
CREATE TRIGGER audit_status AFTER UPDATE OF status ON dgpc.interventions FOR EACH ROW WHEN (OLD.status IS DISTINCT FROM NEW.status) EXECUTE FUNCTION dgpc.audit_fn();
UPDATE dgpc.interventions SET status='closed' WHERE id=7;
SELECT * FROM dgpc.audit;
ROLLBACK;

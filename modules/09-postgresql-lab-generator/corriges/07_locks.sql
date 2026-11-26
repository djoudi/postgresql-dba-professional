\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
-- Session C, pendant que B attend :
SELECT pid,pg_blocking_pids(pid) AS bloqueurs,wait_event FROM pg_stat_activity WHERE datname=current_database() AND cardinality(pg_blocking_pids(pid))>0;

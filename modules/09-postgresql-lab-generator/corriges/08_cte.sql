\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
WITH stats AS (SELECT unit_id,avg(response_minutes) AS moyenne FROM dgpc.interventions GROUP BY unit_id) SELECT *,dense_rank() OVER(ORDER BY moyenne) AS rang FROM stats ORDER BY rang;

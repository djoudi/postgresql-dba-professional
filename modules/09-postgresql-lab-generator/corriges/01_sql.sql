\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
SELECT u.id,u.name,count(i.id),round(avg(i.response_minutes) FILTER (WHERE i.status='closed'),2) FROM dgpc.units u LEFT JOIN dgpc.interventions i ON i.unit_id=u.id GROUP BY u.id,u.name ORDER BY u.id;

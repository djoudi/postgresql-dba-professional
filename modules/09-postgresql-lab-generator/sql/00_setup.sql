\set ON_ERROR_STOP on
DO $$ BEGIN IF current_database() !~ '^lab_[a-z0-9_]+$' THEN RAISE EXCEPTION 'Base de formation obligatoire'; END IF; END $$;
BEGIN;
CREATE SCHEMA dgpc;
CREATE TABLE dgpc.units(id int PRIMARY KEY, name text NOT NULL);
CREATE TABLE dgpc.agents(id int PRIMARY KEY, unit_id int REFERENCES dgpc.units, name text NOT NULL);
CREATE TABLE dgpc.vehicles(id int PRIMARY KEY, unit_id int REFERENCES dgpc.units, code text NOT NULL);
CREATE TABLE dgpc.interventions(id bigint PRIMARY KEY, unit_id int NOT NULL REFERENCES dgpc.units, agent_id int REFERENCES dgpc.agents, vehicle_id int REFERENCES dgpc.vehicles, started_at timestamp NOT NULL, response_minutes int CHECK(response_minutes>=0), status text CHECK(status IN ('open','closed')));
INSERT INTO dgpc.units SELECT g,'Unité '||g FROM generate_series(1,101) g;
INSERT INTO dgpc.agents SELECT g,1+(g-1)%100,'Agent fictif '||g FROM generate_series(1,1000) g;
INSERT INTO dgpc.vehicles SELECT g,1+(g-1)%100,'VEH-'||g FROM generate_series(1,300) g;
INSERT INTO dgpc.interventions SELECT g,1+(g-1)%100,1+(g-1)%1000,1+(g-1)%300,timestamp '2026-01-01'+g*interval '1 minute',5+g%56,CASE WHEN g%7=0 THEN 'open' ELSE 'closed' END FROM generate_series(1,:n) g;
COMMIT;
ANALYZE dgpc.interventions;

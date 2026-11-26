BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT version(),current_database(),pg_is_in_recovery();
SELECT state,count(*) FROM pg_stat_activity GROUP BY state;
SELECT pid,pg_blocking_pids(pid) FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid))>0;
SELECT pg_database.datname,age(datfrozenxid),deadlocks,temp_bytes FROM pg_stat_database JOIN pg_database ON datid=pg_database.oid;
SELECT schemaname,relname,n_dead_tup,last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
ROLLBACK;

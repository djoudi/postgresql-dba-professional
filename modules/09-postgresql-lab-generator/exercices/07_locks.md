# Verrous — trois sessions psql sur la même base lab_
A : `BEGIN; UPDATE dgpc.interventions SET response_minutes=21 WHERE id=1;`
B : `BEGIN; SET LOCAL lock_timeout='30s'; UPDATE dgpc.interventions SET response_minutes=22 WHERE id=1;`
C : exécuter corriges/07_locks.sql pendant l'attente de B. Puis ROLLBACK dans A et B. Ne pas terminer de processus.

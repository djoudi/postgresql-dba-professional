# RB-14 — CPU élevée

## Symptômes
Charge CPU soutenue.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
uptime; ps -eo pid,comm,%cpu --sort=-%cpu | head -20; vmstat 1 3
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT pid,backend_type,state,wait_event FROM pg_stat_activity WHERE state='active';
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Corréler PID OS et activité SQL. Réduire charge non essentielle; tester optimisation des requêtes et concurrence.

## Validation
Comparer CPU et débit à charge comparable.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Baselines et suivi des requêtes coûteuses.

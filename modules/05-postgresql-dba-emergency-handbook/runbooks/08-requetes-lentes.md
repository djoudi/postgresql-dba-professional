# RB-08 — Requêtes lentes

## Symptômes
Latence applicative accrue.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
uptime; vmstat 1 3
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT pid,state,wait_event_type,wait_event,now()-query_start AS age FROM pg_stat_activity WHERE state='active' AND pid<>pg_backend_pid() ORDER BY age DESC LIMIT 20;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier attente ou consommation. Examiner pg_stat_statements si disponible; utiliser EXPLAIN sans ANALYZE sur une requête revue, puis tester les changements hors production.

## Validation
Comparer latences sur charge comparable.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Mesurer percentiles et plans de référence.

# RB-09 — Blocages

## Symptômes
Sessions en attente de verrou.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
uptime
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT pid,pg_blocking_pids(pid) AS bloqueurs,wait_event FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid))>0;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier la transaction racine et son propriétaire. Faire terminer normalement la transaction; annulation ou terminaison ciblée uniquement après autorisation et analyse du rollback.

## Validation
Absence de blocage persistant et reprise métier.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Transactions courtes, ordre de verrouillage cohérent.

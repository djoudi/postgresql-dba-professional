# RB-15 — Pression mémoire / OOM

## Symptômes
Processus tués, swap ou latence.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
free -h; vmstat 1 3; journalctl -k -n 100 --no-pager
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SHOW work_mem; SHOW shared_buffers; SHOW max_connections;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier OOM et concurrence. Réduire charge, examiner work_mem par opération et pools. Ajuster progressivement après test, sans formule universelle.

## Validation
Vérifier absence de nouveaux OOM et stabilité.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Surveiller RSS, swap et concurrence.

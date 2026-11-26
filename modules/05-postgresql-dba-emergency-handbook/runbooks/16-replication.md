# RB-16 — Retard de réplication

## Symptômes
Standby en retard.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_lsclusters; df -h
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT application_name,state,sent_lsn,write_lsn,flush_lsn,replay_lsn FROM pg_stat_replication;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Vérifier réseau, I/O et replay côté standby. Ne pas promouvoir sans fencing et procédure HA; réinitialiser le standby si WAL requis indisponible.

## Validation
Vérifier convergence LSN et lecture sur standby.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Alertes de lag et exercices de bascule.

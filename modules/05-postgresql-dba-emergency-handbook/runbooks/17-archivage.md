# RB-17 — Archivage WAL en échec

## Symptômes
failed_count augmente.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
df -h; pg_lsclusters
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT archived_count,failed_count,last_failed_wal,last_failed_time FROM pg_stat_archiver; SHOW archive_mode;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Vérifier destination, droits, réseau et commande d’archivage. Corriger sans écraser des archives existantes; ne pas effacer WAL en attente.

## Validation
Vérifier nouveaux archivages réussis et chaîne PITR.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Contrôler fraîcheur des archives et espace.

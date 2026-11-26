# RB-07 — Corruption suspectée

## Symptômes
Invalid page, checksum failure.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
journalctl -k -n 100 --no-pager; lsblk
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SHOW data_checksums;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Isoler les écritures, préserver journaux et copie cohérente, vérifier stockage. Restaurer une sauvegarde saine sur une instance séparée; solliciter expertise. Ne pas utiliser pg_resetwal comme réparation courante.

## Validation
Contrôles métier et intégrité sur instance restaurée.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Checksums, sauvegardes testées, surveillance stockage.

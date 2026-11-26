# RB-06 — Croissance WAL

## Symptômes
Le répertoire WAL augmente.

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
SELECT slot_name,active,restart_lsn FROM pg_replication_slots; SELECT * FROM pg_stat_archiver;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier slot retardé, archivage en échec ou forte activité. Réparer le consommateur ou archivage. Supprimer un slot seulement après accord et plan de resynchronisation.

## Validation
Vérifier progression des LSN et stabilisation du volume.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Surveiller slots, archivage et capacité.

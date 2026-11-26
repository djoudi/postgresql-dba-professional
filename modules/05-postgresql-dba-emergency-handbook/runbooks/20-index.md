# RB-20 — Index suspect ou invalide

## Symptômes
Plan dégradé ou index invalide.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
df -h
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT indexrelid::regclass,indisvalid,indisready FROM pg_index WHERE NOT indisvalid OR NOT indisready;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier origine et dépendances. Tester REINDEX CONCURRENTLY si applicable, avec espace et fenêtre suffisants; ne pas supprimer un index sur seul critère idx_scan.

## Validation
Vérifier validité et plans après opération.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Contrôler migrations et créations concurrentes.

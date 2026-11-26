# RB-05 — Disque plein

## Symptômes
No space left on device.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
df -h; df -i; lsblk
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT datname,pg_database_size(datname) FROM pg_database WHERE datallowconn;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Suspendre les écritures non essentielles. Étendre le volume ou déplacer des fichiers non PostgreSQL identifiés selon procédure. Ne jamais supprimer pg_wal ou les fichiers de données.

## Validation
Vérifier espace et inodes, reprise des écritures et journaux.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Alertes sur espace, inodes et croissance.

# RB-12 — Échec de restauration

## Symptômes
pg_restore signale des erreurs.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_restore --version; df -h
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT version(); SELECT extname,extversion FROM pg_extension;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Vérifier version, extensions, rôles et catalogue pg_restore --list. Repartir sur une nouvelle base isolée avec --exit-on-error --single-transaction lorsque compatible.

## Validation
Vérifier objets, contraintes, données et droits.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Tester restauration avant incident.

# RB-23 — Droits insuffisants

## Symptômes
Permission denied.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_lsclusters
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT current_user,session_user; SELECT nspname,nspacl FROM pg_namespace WHERE nspname NOT LIKE 'pg_%';
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Identifier rôle effectif, objet et privilège requis. Accorder uniquement le droit nécessaire après validation; ne pas donner SUPERUSER pour résoudre un refus.

## Validation
Tester avec le rôle applicatif et vérifier refus hors périmètre.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Matrice des droits et tests de régression.

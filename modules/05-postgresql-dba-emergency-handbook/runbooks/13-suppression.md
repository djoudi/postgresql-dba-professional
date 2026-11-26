# RB-13 — Suppression accidentelle

## Symptômes
Données ou table supprimées.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
date -u; pg_lsclusters
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT now(),pg_is_in_recovery();
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Suspendre les écritures concernées et noter heure UTC. Restaurer sauvegarde et WAL disponibles vers une instance isolée avant la suppression; extraire les données nécessaires après validation métier.

## Validation
Comparer données récupérées et changements légitimes ultérieurs.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
PITR testé, privilèges minimaux, validation des migrations.

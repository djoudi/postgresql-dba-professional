# RB-18 — Autovacuum insuffisant

## Symptômes
Dead tuples et tables en croissance.

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
SELECT schemaname,relname,n_live_tup,n_dead_tup,last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Rechercher transactions anciennes et paramètres par table. Planifier VACUUM ciblé après analyse; éviter VACUUM FULL en urgence sans fenêtre et espace.

## Validation
Vérifier statistiques, latence et évolution des tuples morts.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Suivre autovacuum et transactions longues.

# RB-04 — Saturation des connexions

## Symptômes
Too many clients already.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_lsclusters; free -h
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT state,count(*) FROM pg_stat_activity GROUP BY state; SHOW max_connections;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Limiter les nouvelles demandes côté application, examiner les pools et sessions inactives. Ne terminer une session qu’après validation du propriétaire.

## Validation
Vérifier les connexions disponibles et les erreurs applicatives.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Dimensionner les pools et réserver une voie DBA.

# RB-19 — Risque de wraparound

## Symptômes
Âge XID élevé, avertissements.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_lsclusters; df -h
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT datname,age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Escalader rapidement. Identifier transactions anciennes et tables à âge élevé; permettre vacuum anti-wraparound, planifier VACUUM FREEZE ciblé avec DBA. Ne pas désactiver autovacuum.

## Validation
Vérifier baisse de l’âge XID et journaux.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Alertes selon autovacuum_freeze_max_age.

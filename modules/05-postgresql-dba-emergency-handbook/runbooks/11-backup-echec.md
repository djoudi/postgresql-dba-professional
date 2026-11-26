# RB-11 — Échec de sauvegarde

## Symptômes
pg_dump retourne un code non nul.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
df -h; df -i; pg_dump --version
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT version();
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Conserver la dernière sauvegarde valide. Vérifier droits, espace, version client et connectivité; relancer vers un nouveau fichier temporaire, vérifier code retour et catalogue.

## Validation
Test de restauration isolé et contrôle métier.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Alertes sur échec et âge de dernière sauvegarde.

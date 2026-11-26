# RB-22 — Configuration invalide

## Symptômes
Erreur après changement.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
pg_lsclusters; journalctl -u postgresql@18-main -n 100 --no-pager
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT sourcefile,sourceline,name,error FROM pg_file_settings WHERE error IS NOT NULL;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Comparer avec copie approuvée, corriger ou restaurer uniquement les fichiers concernés. Recharger ou redémarrer selon contexte du paramètre.

## Validation
Vérifier pg_settings, pending_restart et connexion.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Versionner configurations sans secrets.

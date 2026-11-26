# RB-03 — Échec de connexion

## Symptômes
Password authentication failed ou no pg_hba.conf entry.

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
SELECT line_number,type,database,user_name,address,auth_method,error FROM pg_hba_file_rules;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Vérifier la première règle applicable, le rôle et la méthode. Corriger la règle minimale, vérifier les erreurs puis recharger. Réinitialiser le secret via \password si nécessaire.

## Validation
Tester une nouvelle connexion autorisée et un refus attendu.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Utiliser SCRAM et gérer les secrets hors scripts.

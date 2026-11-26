# RB-21 — Échec TLS

## Symptômes
Certificat expiré ou non vérifiable.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
date -u; openssl version
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SHOW ssl; SHOW ssl_cert_file;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Vérifier chaîne, SAN, date et permissions de clé. Remplacer via procédure approuvée et recharger si applicable. Ne pas désactiver la vérification client.

## Validation
Connexion avec sslmode=verify-full et CA attendue.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Alertes expiration et renouvellement testé.

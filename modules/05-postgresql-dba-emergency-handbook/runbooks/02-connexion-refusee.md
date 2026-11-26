# RB-02 — Connexion TCP refusée

## Symptômes
Le client reçoit connection refused.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
ss -lnt; pg_lsclusters; pg_isready -h 127.0.0.1 -p 5432
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SHOW listen_addresses; SHOW port;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Comparer adresse, port et écoute réelle. Corriger la cible ou la configuration approuvée; ne pas ouvrir toutes les interfaces par défaut.

## Validation
Tester depuis le réseau autorisé puis avec psql.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Documenter les ports et règles réseau.

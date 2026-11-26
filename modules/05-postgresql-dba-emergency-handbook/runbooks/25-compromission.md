# RB-25 — Compromission suspectée

## Symptômes
Connexion ou rôle inattendu.

## Triage et périmètre
Noter heure UTC, cluster, base, impact métier, dernier changement et responsable. En cas de perte de données, suspicion de compromission ou indisponibilité critique, escalader immédiatement. Préserver les preuves avant toute modification.

## Diagnostic système (lecture seule)
Adapter 18-main et 5432 au cluster réel. Les journaux peuvent contenir des secrets : accès restreint.
```bash
date -u; ss -nt; journalctl -u postgresql@18-main -n 100 --no-pager
```

## Diagnostic SQL
Exécuter via psql -X avec le rôle autorisé, dans une transaction en lecture seule. Si le serveur est arrêté, passer au diagnostic système.
```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout='10s';
SET LOCAL lock_timeout='2s';
SELECT rolname,rolsuper,rolcreaterole,rolcanlogin FROM pg_roles; SELECT pid,usename,client_addr,backend_start FROM pg_stat_activity;
ROLLBACK;
```

## Remédiation et reprise (manuelle)
Activer réponse à incident, isoler via équipe sécurité, préserver preuves et journaux. Révoquer accès compromis et renouveler secrets selon plan coordonné; restaurer depuis source saine si nécessaire.

## Validation
Valider intégrité, accès et surveillance avant réouverture.

## Retour arrière
Avant changement, conserver configuration et état de référence. Si la validation échoue, arrêter les changements, restaurer la configuration approuvée si applicable et escalader. Ne pas écraser les données actives; privilégier une instance de reprise séparée.

## Prévention
Moindre privilège, segmentation, audit et rotation des secrets.

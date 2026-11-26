# Reprise et restauration
RPO : perte de données maximale acceptable. RTO : délai maximal acceptable de reprise. Les objectifs sont fixés par le métier.
## Sauvegarde logique de confiance
Sur une instance de test isolée, avec un compte autorisé et une archive provenant d’une source fiable :
```bash
pg_restore --list sauvegarde.dump
createdb -T template0 reprise_test
pg_restore --exit-on-error --single-transaction --no-owner --no-privileges -d reprise_test sauvegarde.dump
```
Vérifier le code retour, extensions, objets, volumes, contraintes et tests métier. Les propriétaires et ACL doivent être traités séparément. Une archive peut contenir du code SQL exécutable : ne jamais restaurer une archive non fiable. Ne pas utiliser une base existante. En cas d’échec, conserver les traces et recommencer dans une autre base neuve.
## PITR
Exige une sauvegarde physique compatible et une chaîne WAL complète. Sur hôte isolé, restaurer selon la documentation de l’outil de sauvegarde, configurer restore_command, recovery_target_time avec fuseau explicite et recovery.signal. Valider le point de reprise avant promotion. Ne jamais réutiliser le répertoire actif. Prévoir fencing et bascule approuvée. Sans chaîne WAL, le PITR n’est pas garanti.
## Références
- https://www.postgresql.org/docs/current/backup.html
- https://www.postgresql.org/docs/current/continuous-archiving.html
- https://www.postgresql.org/docs/current/monitoring-stats.html

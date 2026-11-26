# Guide d’exploitation

1. Identifier le cluster avec `pg_lsclusters` sur Debian/Ubuntu.
2. Choisir la base et le port explicitement.
3. Exécuter le script version puis les diagnostics ciblés.
4. Comparer les compteurs sur deux intervalles et vérifier stats_reset.
5. Conserver les résultats dans un dossier privé.
6. Confirmer les hypothèses avant toute correction.

Les scripts utilisent des transactions en lecture seule et des délais locaux. Cela ne supprime pas les coûts de lecture ni les verrous de consultation. Les statistiques de tables concernent la base courante. Les statistiques de sessions peuvent être masquées selon les droits. Les vues HBA et WAL nécessitent des droits particuliers. Les scripts ne collectent pas les mots de passe ni le texte des requêtes.

## Validation
Le contrôle Python vérifie le nombre et les garde-fous textuels, pas la syntaxe SQL ni les résultats. Tester chaque requête sur une VM PostgreSQL 14 à 18 avant production.

Documentation officielle : https://www.postgresql.org/docs/18/monitoring-stats.html

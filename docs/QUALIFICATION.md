# Qualification avant publication
## Matrice à exécuter
PostgreSQL 14, 15, 16, 17, 18 : workflow integration.yml, bibliothèque SQL et restauration de 1000 lignes. Les résultats CI ne sont pas encore disponibles. Pour chaque couple source <= cible, utiliser les clients de la cible, deux instances jetables, vérifier extensions, locale, contenu, ACL et application. Tester aussi échec de restauration et conservation de la source.
## Ubuntu 22.04 / 24.04 / 26.04
Pour chaque VM : snapshot, console ouverte, compte administrateur non-root, test SSH avant/après, attendre le rollback sans confirmer puis vérifier une nouvelle connexion. Tester socket activation, UFW, Fail2Ban, installation et rollback de configuration PostgreSQL. Ne jamais exécuter ces tests sur le poste de production.
## Critères de sortie
Toutes les suites locales et CI réussies; preuves de restauration et de migration; tests VM documentés; revue des droits; licence approuvée. En cas d'échec, conserver le statut RC. Aucun test de charge à 10 millions de lignes n'est attesté.

# Audit de consolidation
Les dix ZIP originaux ont été ouverts et leur CRC vérifié. Les répertoires sources correspondants ont été copiés, sans caches ni workflows imbriqués. Les tests locaux sont structurels, unitaires ou simulés; aucun serveur PostgreSQL ni VM systemd n’est disponible. Les anciens rapports de tests des modules restent historiques.

## Corrections ciblées
- Migration : exclusion littérale des schémas pg_, comptage ONLY pour éviter les doubles comptages liés à l’héritage, restauration sans tablespaces source.
- Lab : createdb sans invite de mot de passe, chemins d’archives absolus pour pg_restore.
- Déploiement : authentification peer/SCRAM explicite à la création du cluster.

## Risques résiduels
- SQL library : structure vérifiée, SQL non exécuté.
- Backup : vérification d’intégrité simulée, restauration réelle non validée.
- Security/Performance/Health : visibilité dépendante des droits, statistiques cumulatives, pas de certification.
- Emergency : procédures à adapter au contexte et aux sauvegardes.
- Deployment : modifications concurrentes non protégées; rollback limité aux fichiers; tester en VM.
- Ubuntu security : timer transitoire, pas de garantie de retour SSH; ne pas lancer deux changements simultanés, garder console et session de secours.
- Lab : préfixe seul insuffisant, volume de 10 millions non testé.
- Migration : arrêt des écritures déclaratif, ACL non restaurées, comptages non équivalents à une comparaison de contenu, compatibilité locale/extension à valider. Ne pas ouvrir la cible avant revue des droits.

Revue ciblée et tests de régression, pas audit exhaustif ligne par ligne ni homologation. Workflows originaux remplacés par un workflow commun hors serveur; les tests d’intégration restent à réaliser.

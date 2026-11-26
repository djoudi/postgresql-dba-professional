# Guide du formateur
## Préparation
VM dédiée, PostgreSQL installé, rôle LOGIN CREATEDB non superutilisateur, authentification locale configurée. Vérifier `pg_lsclusters`, `psql --version`, `df -h`. Les clients pg_dump doivent être au moins aussi récents que le serveur. Pour une connexion distante utiliser PGSSLMODE=verify-full et un certificat de confiance.
## Volumes
1 000 : initiation; 10 000 : SQL; 100 000 : index; 1 000 000 : performance; 10 000 000 : test de charge sur VM dimensionnée. Les tailles et durées dépendent du matériel; prévoir plusieurs Gio libres et de la marge WAL. Ne pas lancer les gros volumes sur production. Les données sont déterministes, 101 unités dont une vide, 1000 agents, 300 véhicules, N interventions, floor(N/7) ouvertes. La distribution est volontairement simplifiée.
## Validation
Comparer count(*) à N, vérifier les clés étrangères et les unités sans intervention. EXPLAIN ANALYZE exécute réellement la requête; ici SELECT seulement. Un index peut être ignoré sur une petite table. Pour les verrous, utiliser trois sessions, timeout et rollback. Pour restaurer, utiliser uniquement une archive de confiance et une instance isolée : un dump peut contenir du code SQL. Aucun nettoyage automatique. En cas de panne, inspecter la base partielle; ne la supprimer qu'après identification et autorisation.
## Évaluation /20
SQL et CTE 4; index et plans 4; routines et audit 4; transactions et verrous 4; sauvegarde et validation 4. Exiger les preuves et l'interprétation, pas uniquement les commandes.

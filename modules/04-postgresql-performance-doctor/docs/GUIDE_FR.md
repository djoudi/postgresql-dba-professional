# Guide d'exploitation
## Préparation
Installer Python et psql. Utiliser un compte autorisé à se connecter à la base. Pour une visibilité étendue, un DBA peut accorder pg_monitor à un rôle dédié après analyse des risques. Ne pas utiliser root. Pour un serveur distant, configurer PGSSLMODE=verify-full, PGSSLROOTCERT et un fichier .pgpass mode 0600. Ne jamais passer un mot de passe en argument. Les paramètres libpq de l'environnement restent applicables; vérifier la cible affichée dans le rapport.
## Interprétation
- Connexions: comparer au maximum et aux connexions réservées; mesurer les pics.
- Transactions et blocages: examiner les PID, l'application et la durée; ne pas tuer automatiquement une session.
- Cache: ratio cumulatif, ne représente pas le cache du système.
- Tuples morts: estimations, pas mesure exacte du bloat. Comparer les captures et les seuils par table.
- Autovacuum: examiner dates, compteurs et modifications; une date NULL peut être normale. Vérifier aussi les workers et l'âge XID.
- Index: idx_scan faible ne prouve pas l'inutilité. Examiner contraintes, charge et réinitialisation des statistiques.
- Scans séquentiels: parfois préférables aux index. Tester EXPLAIN sur une requête autorisée; EXPLAIN ANALYZE exécute réellement la requête.
- Requêtes: total_ms mesure le coût cumulé, mean_ms la moyenne, calls la fréquence. Le queryid peut être absent selon les droits. Les statistiques ne sont pas un journal exhaustif. L'extension pg_stat_statements nécessite une configuration préalable par le DBA; Doctor ne l'installe pas.
- Fichiers temporaires: comparer les deltas; work_mem est par opération et peut se multiplier avec le parallélisme.
- Age XID: comparer aux seuils de gel, traiter les transactions longues et surveiller le vacuum.
## Sécurité et limites
Transactions READ ONLY, délais de requête 10 s et verrou 2 s, délai processus 20 s par contrôle. Rapports locaux privés, sans texte des requêtes. Les noms des objets et PID restent sensibles. Les contrôles sont indépendants, non atomiques et limités en lignes. Les statistiques peuvent être masquées par les droits. La lecture peut consommer des ressources et prendre des verrous de lecture. Pas de diagnostic automatique du matériel ni de mesure du bloat exact. Aucun score de santé artificiel. Vérifier les recommandations avec des mesures répétées.
## Dépannage
Tester `psql -X -w -p 5432 -d postgres -c 'SELECT version()'`. En cas de UNKNOWN, vérifier droits, extension, délais et version. Ne pas augmenter les privilèges sans justification. Les erreurs détaillées de psql ne sont pas exportées pour limiter la fuite de données.

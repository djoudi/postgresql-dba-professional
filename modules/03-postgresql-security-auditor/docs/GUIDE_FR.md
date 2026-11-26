# Guide d'exploitation
## Préparation
Installer python3 et postgresql-client via les dépôts approuvés. Utiliser pg_lsclusters pour identifier le port. Pour chaque base applicative, lancer un audit distinct : les ACL et fonctions sont propres à la base. Le mode interactif affiche les clusters locaux, puis demande port, base et dossier. Le mode CLI accepte aussi --host et --user. Pour une connexion distante, configurer PGSSLMODE=verify-full et PGSSLROOTCERT avec une autorité approuvée. Utiliser peer ou un fichier .pgpass protégé (0600); aucun mot de passe en argument.
## Privilèges
Un rôle de supervision pg_monitor peut lire une partie des statistiques. Les vues pg_hba_file_rules, pg_file_settings et pg_authid peuvent nécessiter des droits supplémentaires. Ne pas accorder un accès global à pg_authid uniquement pour cet outil : accepter UNKNOWN ou faire exécuter ponctuellement par un DBA habilité. Aucun rôle n'est créé par l'outil.
## Lecture des résultats
OK signifie uniquement zéro élément détecté par la requête. REVIEW demande une analyse humaine, HIGH indique une priorité indicative, INFO est un inventaire, UNKNOWN indique une collecte impossible ou non compatible. Les superutilisateurs légitimes, connexions locales et règles historiques ne constituent pas automatiquement des vulnérabilités. Les règles HBA lues sur disque peuvent différer de celles chargées. TLS activé ne garantit pas TLS obligatoire. Les ACL indirectes et politiques RLS ne sont pas auditées exhaustivement. Les contrôles ne remplacent ni un audit réseau ni une analyse des versions corrigées.
## Sécurité et exploitation
Les sessions psql désactivent les fichiers de démarrage et imposent default_transaction_read_only, statement_timeout 10s, lock_timeout 2s. Chaque contrôle est une connexion distincte : pas de photographie transactionnelle globale. Les rapports contiennent des informations d'infrastructure, à conserver en accès restreint. Aucune remédiation automatique. Examiner les résultats, sauvegarder les configurations, tester les corrections sur une VM et vérifier les accès avant production.
## Automatisation
Exemple crontab du compte de supervision, après création du dossier privé et validation de l'authentification non interactive :
```
0 7 * * 1 /opt/pg-auditor/auditor.sh --port 5432 --database postgres --output /var/lib/pg-audit
```
Surveiller les codes retour 1 et 2; définir une rétention selon la politique interne. Aucun cron installé automatiquement.
## Validation
python3 -m unittest discover -s tests -v ; bash -n auditor.sh. Les tests locaux simulent psql. La CI fournit un test PostgreSQL 18 réel, à exécuter sur GitHub. Tester aussi 14–17 et les permissions restreintes avant diffusion en production.

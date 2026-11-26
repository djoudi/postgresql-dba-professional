# Guide d'exploitation
## Préparation
Installer Python 3 et psql. Utiliser un compte de surveillance dédié avec CONNECT sur la base et, si autorisé, pg_monitor. Ce rôle expose des métadonnées sensibles. Certaines vues HBA nécessitent des droits supplémentaires; ne pas accorder superuser uniquement pour obtenir un rapport complet. Utiliser peer ou .pgpass (0600), jamais un mot de passe en argument. Pour un serveur distant, définir PGSSLMODE=verify-full et PGSSLROOTCERT vers la CA approuvée.
## Périmètre
Choisir le port après pg_lsclusters. Le rapport SQL porte sur une seule connexion et les statistiques des tables/index sur la base sélectionnée. Relancer pour chaque base. L'inventaire local n'est pas celui du serveur distant. Les requêtes sont indépendantes, non atomiques, limitées à 10 secondes et aux verrous de 2 secondes. Aucun texte de requête ni hash de mot de passe exporté.
## Lecture
- Connexions : rapprocher clients et maximum, tenir compte des connexions réservées.
- Cache : ratio cumulé depuis reset; un ratio élevé ne garantit pas de bonnes latences.
- Verrous et transactions : identifier le propriétaire avant intervention.
- Tables : n_dead_tup est une estimation, vérifier autovacuum et charge avant VACUUM.
- Index : idx_scan faible ne justifie pas DROP INDEX; examiner contraintes et période observée.
- Gel : comparer age_xid au seuil configuré et investiguer les transactions anciennes.
- TLS et HBA : examiner la politique réseau et les règles effectives; un compteur trust ne prouve pas une exposition externe.
- Archivage et réplication : vérifier les objectifs RPO/RTO et les sauvegardes restaurables séparément.
- Disques : vérifier aussi les tablespaces, inodes et volumes distants.
## Rapports
HTML hors ligne, JSON structuré, CSV avec colonne JSON pour conserver les types. Dossier privé 0700, fichiers 0600. Protéger les rapports contenant noms de bases, objets et topologie. Pas de score arbitraire. OK = collecte réussie; UNKNOWN = collecte impossible. Codes 0 complet, 2 partiel, 1 échec de connexion ou d'exécution (argparse peut retourner 2 pour une erreur CLI).
## Dépannage
Vérifier psql, pg_isready, port, socket, droits et certificat. Une absence de lignes n'est pas une preuve de bonne santé. Comparer des rapports pris dans des conditions similaires; les compteurs peuvent être réinitialisés. Ne pas automatiser de correction à partir de ces résultats.

# Guide d'exploitation

## Préparation
Identifier le cluster avec `pg_lsclusters`, vérifier l'espace libre (`df -h`), le compte postgres et l'accès local peer. Installer avec `sudo bash install.sh`. Le répertoire doit être canonique, appartenir à postgres et être en mode 0700. Ne pas utiliser un répertoire partagé ou un chemin dont un parent est modifiable par un tiers.

## Sauvegarde
`sudo -u postgres pg-backup-guardian backup 18 main ma_base /var/lib/postgresql/guardian-backups`
Le résultat est un dossier horodaté UTC contenant database.dump (format custom), catalogue.txt, globals.sql (sans mots de passe), manifest.txt et SHA256SUMS. Une sauvegarde logique est cohérente pour une base ; les objets globaux sont exportés séparément et ne constituent pas un instantané atomique avec celle-ci. Les échecs avant publication laissent au plus un dossier temporaire en cas d'arrêt brutal. Le verrou empêche les sauvegardes simultanées dans un même répertoire.

## Vérification et restauration
`sudo -u postgres pg-backup-guardian verify /chemin/du/dossier`
Vérifie les quatre empreintes ; ne prouve pas l'authenticité ni la restaurabilité. Tester ensuite sur un serveur isolé :
`sudo -u postgres pg-backup-guardian restore 18 main /chemin/du/dossier guardian_restore_test`
La base doit être nouvelle. Les propriétaires et ACL ne sont pas restaurés. Les extensions nécessaires doivent être installées. Les rôles globaux ne sont jamais appliqués automatiquement. En cas d'échec, la base créée reste pour diagnostic. Comparer les données, contraintes, séquences, routines et résultats métier ; le nombre de tables seul ne suffit pas. Mesurer la durée et consigner le RTO.

## Rétention
`sudo -u postgres pg-backup-guardian retention-plan /var/lib/postgresql/guardian-backups 30`
Liste les dossiers candidats selon leur mtime ; aucune suppression. Vérifier les copies hors site et les restaurations avant toute suppression manuelle.

## Dépannage
Connexion refusée : vérifier cluster, port, socket local et pg_hba.conf. Échec de dump : consulter stderr, espace disque et droits. Échec de restauration : vérifier version, extensions et journal ; ne pas écraser une base existante. Empreinte incorrecte : isoler l'archive et rechercher une copie saine.

# Guide d'exploitation
## Préparation
Vérifier `/etc/os-release`, `free -m`, `df -h`, `ss -lntp`, `apt-cache policy postgresql-18`. Ubuntu 22.04/24.04/26.04 et Debian sont ciblés; la disponibilité des versions dépend des dépôts. Utiliser le dépôt PGDG officiel selon sa documentation si nécessaire: https://www.postgresql.org/download/linux/ubuntu/ ou https://www.postgresql.org/download/linux/debian/. Ne jamais désactiver la vérification des signatures.
## Déploiement
Exécuter les commandes du README sans --apply puis avec --apply. Vérifier le port et le nom avant confirmation. `status`, `start`, `stop`, `restart` utilisent pg_ctlcluster. Aucun effacement de cluster n'est proposé.
## Mémoire
shared_buffers: 25% de la RAM déclarée, plafonné à 8 Gio; effective_cache_size: 50%, estimation et non allocation; work_mem: 4 Mio par opération; maintenance_work_mem: 1/16, plafonné à 512 Mio. Utiliser --ram pour le budget réellement disponible, notamment VM/conteneur ou plusieurs clusters. Mesurer avant d'ajuster.
## Authentification
Le profil local ne permet pas les connexions distantes. Créer les rôles applicatifs avec privilèges minimaux et définir les mots de passe via \password dans psql. Ne pas mettre de secret dans la ligne de commande. Les anciens secrets MD5 ne sont pas convertis automatiquement. Pour accès distant, concevoir séparément TLS, règles hostssl ciblées et pare-feu. Aucun changement automatique de pare-feu.
## Validation
Vérifier pg_lsclusters, pg_isready -h /var/run/postgresql -p 5435, puis sudo -u postgres psql -p 5435 -d postgres. Contrôler SHOW listen_addresses; SHOW password_encryption; SELECT * FROM pg_hba_file_rules WHERE error IS NOT NULL;. Tester le compte applicatif. Les fichiers inclus et ALTER SYSTEM peuvent surcharger les paramètres; examiner pg_settings et pg_file_settings.
## Retour arrière
Le chemin de sauvegarde est affiché lors de configure. En cas d'échec, le programme tente de restaurer les deux fichiers et redémarrer. Si cela échoue, utiliser la console et examiner journalctl -u postgresql@18-formation. Pour restauration manuelle: sudo ./wizard.sh rollback --version 18 --cluster formation --backup /var/backups/pg-deployment-wizard/18-formation/HORODATAGE --apply. Le rollback ne restaure ni données ni paquets, ni fichiers externes. Sauvegarder le serveur avant intervention. Ne pas lancer deux modifications simultanées. Le profil suppose une configuration Debian standard et un rôle postgres local accessible.
## Tests
python3 -m unittest discover -s tests -v. Tester sur VM jetable avant production. Les tests unitaires ne remplacent pas un test d'installation et de restauration réel.

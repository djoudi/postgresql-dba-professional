# Guide d'exploitation
## Préparation
Disposer d'une console hyperviseur, d'une sauvegarde et d'une deuxième session SSH. Vérifier `sshd -T`, `systemctl status ssh.service ssh.socket`, `ss -lntp`. Ne pas modifier les ports à distance sans procédure dédiée. Le profil conserve le port et les méthodes d'authentification existantes sauf accès root et mots de passe vides. Les directives Match et les fichiers prioritaires peuvent modifier le résultat effectif.
## Clés publiques
Générer sur le poste client `ssh-keygen -t ed25519`. Transférer uniquement le fichier .pub. Vérifier son empreinte par canal indépendant. Utiliser key-add avec --apply après simulation. Tester `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 admin@serveur`. Ne jamais transférer la clé privée. Vérifier `namei -l /home/admin/.ssh/authorized_keys`. La révocation est manuelle après sauvegarde du fichier et identification de l'empreinte.
## SSH et retour arrière
Utiliser un compte non root avec sudo vérifié. Le profil interdit root, limite les tentatives et désactive X11. Le timer transitoire systemd restaure le fichier après cinq minutes sauf annulation explicite. Tester une nouvelle connexion, vérifier `sudo -v` et les paramètres effectifs `sudo sshd -T -C user=admin,host=client,addr=192.168.10.50`. Annuler uniquement le timer affiché si tous les tests réussissent. Ne pas redémarrer le système pendant la fenêtre : le timer transitoire ne survit pas au reboot. En cas d'échec, attendre le retour ou utiliser la console et `sudo ./toolkit.sh rollback --backup /var/backups/ubuntu-security-toolkit/ssh-XXXX --apply`. Ce mécanisme ne garantit pas la récupération en cas de panne systemd, disque ou réseau. Le service SSH doit être actif; le port/socket n'est pas modifié.
## Pare-feu
Inventorier `sudo ufw status numbered` et les services. Ajouter une autorisation pour le CIDR d'administration avec ufw-allow. Vérifier le port réel et les règles existantes. L'activation UFW et la suppression de règles restent manuelles depuis la console, après autorisation de tous les flux nécessaires. Ne pas exposer PostgreSQL publiquement.
## Fail2Ban
Installer avec `sudo ./toolkit.sh fail2ban --apply`. Examiner `/etc/fail2ban/jail.conf` et les fichiers jail.d. Exemple à adapter dans un fichier local :
```ini
[sshd]
enabled = true
backend = systemd
maxretry = 5
findtime = 10m
bantime = 1h
```
Valider `sudo fail2ban-client -t`, puis recharger le service depuis la console. Vérifier `sudo fail2ban-client status sshd`. Adapter le port réel et vérifier le journal. Ne pas bannir le réseau d'administration par erreur.
## Mises à jour
Installer unattended-upgrades via updates --apply. Vérifier les origines autorisées dans `/etc/apt/apt.conf.d/50unattended-upgrades`, configurer la périodicité avec `sudo dpkg-reconfigure unattended-upgrades`, tester `sudo unattended-upgrade --dry-run --debug`. Prévoir une fenêtre de maintenance et vérifier les besoins de redémarrage. Le toolkit ne lance pas de mise à niveau globale.
## Audit
Le rapport HTML/JSON contient des sorties brutes, pas un score de conformité. Vérifier les comptes UID 0, les membres sudo, les comptes inutilisés, les sockets exposés, les échecs de services et les mises à jour. Les erreurs de collecte sont INCONNU. Ne pas diffuser les rapports sans revue.
## Validation
Tester dans chaque version Ubuntu cible : installation, connexion par clé, timer non confirmé, timer confirmé, rollback manuel, service SSH avec socket activation, règles UFW et collecte sans privilèges. Les tests unitaires ne remplacent pas ces essais.

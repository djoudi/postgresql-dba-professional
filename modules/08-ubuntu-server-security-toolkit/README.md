# Ubuntu Server Security Toolkit Premium
Version 1.0.0 — Ubuntu 22.04, 24.04 et 26.04 (cibles, non certifiées).

Prérequis : Python 3, systemd, OpenSSH serveur pour les opérations SSH. UFW et APT selon les commandes. Exécuter d'abord dans une VM avec console. Aucun changement système sans `--apply` (audit écrit uniquement ses rapports).

```bash
./toolkit.sh detect
./toolkit.sh interactive
sudo ./toolkit.sh audit --output /root/security-reports
./toolkit.sh ssh
sudo ./toolkit.sh ssh --apply
./toolkit.sh key-add --user admin --key admin.pub
sudo ./toolkit.sh key-add --user admin --key admin.pub --apply
./toolkit.sh ufw-allow --source 192.168.10.50/32 --port 22
./toolkit.sh fail2ban
./toolkit.sh updates
```
Voir [guide](docs/GUIDE_FR.md). Les commandes fail2ban et updates installent les paquets uniquement; la politique est à configurer séparément. UFW ajoute une règle mais ne l'active pas. Aucun changement de port SSH ni désactivation automatique des mots de passe. Le rollback concerne exclusivement le fichier SSH géré. Ne pas lancer plusieurs modifications simultanées. Les rapports contiennent des informations confidentielles.

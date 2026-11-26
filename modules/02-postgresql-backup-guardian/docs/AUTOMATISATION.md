# Automatisation systemd

Après installation, adapter config/guardian.conf.example à une base existante. Le service fourni utilise le répertoire par défaut ; adapter ReadWritePaths si nécessaire.

```bash
sudo install -m 600 config/guardian.conf.example /etc/pg-backup-guardian.conf
sudoedit /etc/pg-backup-guardian.conf
sudo install -m 644 systemd/guardian-backup.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start guardian-backup.service
sudo journalctl -u guardian-backup.service -n 100 --no-pager
sudo systemctl enable --now guardian-backup.timer
systemctl list-timers guardian-backup.timer
```

Exécution quotidienne à 02h00 heure locale avec délai aléatoire maximal de cinq minutes. Persistent rattrape une échéance manquée. Pour une fréquence hebdomadaire ou mensuelle, modifier OnCalendar via un drop-in (réinitialiser d'abord OnCalendar=). Pour plusieurs bases, créer des unités et fichiers de configuration distincts. Surveiller les échecs via systemd et votre supervision existante. Aucune notification externe intégrée. Désactivation : `sudo systemctl disable --now guardian-backup.timer`. Ne pas supprimer les archives lors de la désinstallation.

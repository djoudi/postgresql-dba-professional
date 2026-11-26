# PostgreSQL Backup Guardian — Premium 1.0.0

Outil Bash de sauvegarde logique locale pour Ubuntu/Debian avec `postgresql-common`. Cible PostgreSQL 14–18, à valider sur chaque version. Aucun mot de passe enregistré. Exécution sous le compte système postgres (authentification peer locale). Les noms de bases simples ASCII sont pris en charge.

## Démarrage

```bash
sudo bash install.sh
sudo -u postgres /usr/local/sbin/pg-backup-guardian interactive
```

Exemple :
```bash
sudo -u postgres /usr/local/sbin/pg-backup-guardian backup 18 main ma_base /var/lib/postgresql/guardian-backups
```

Voir [guide](docs/GUIDE_FR.md), [automatisation](docs/AUTOMATISATION.md), [sécurité](docs/SECURITE.md), [validation](docs/VALIDATION.md). Les archives contiennent des données sensibles. Ne jamais les publier sur GitHub.

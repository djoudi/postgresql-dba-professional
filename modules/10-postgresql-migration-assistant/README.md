# PostgreSQL Migration Assistant Premium
Migration logique hors ligne, PostgreSQL 14–18, vers une base neuve. Python 3 et clients PostgreSQL de la version cible. Aucun mot de passe dans les arguments. Utiliser des services libpq dans ~/.pg_service.conf et ~/.pgpass (0600), TLS verify-full pour les serveurs distants.

```ini
[source]
host=source.example.org
port=5432
user=migrateur
sslmode=verify-full
[target]
host=cible.example.org
port=5432
user=migrateur
sslmode=verify-full
```

```bash
./migrate.sh assess --database application --destination application_new --output assessment
./migrate.sh migrate --database application --destination application_new --output simulation
# Après arrêt des écritures et validation du plan :
./migrate.sh migrate --database application --destination application_new --output migration --source-frozen --apply
./migrate.sh verify --database application --destination application_new --output verification
./migrate.sh interactive
```

Les dossiers doivent être nouveaux. Le mode simulation interroge les serveurs et écrit un rapport local, sans modifier PostgreSQL. Les rapports contiennent des noms et ACL sensibles. Ne pas publier. Code 0 = collecte ou comptages réussis, 1 = erreur, 2 = blocage ou différence. Voir docs/GUIDE_FR.md et docs/ROLLBACK.md.

# PostgreSQL Health Report — Premium 1.0.0
Inventaire local et diagnostic SQL en lecture seule. Cible PostgreSQL 14–18, Ubuntu 22.04–26.04 et Debian. Aucun module Python externe.

```bash
sudo apt install python3 postgresql-client
./health.sh
./health.sh --port 5432 --database postgres --output "$HOME/health-reports"
```
Rapports HTML autonomes avec graphiques à barres, JSON et CSV (une ligne par résultat). Voir [guide](docs/GUIDE_FR.md) et [automatisation](docs/AUTOMATISATION.md). Les contrôles OK signifient collecte réussie, pas conformité. Les statistiques sont ponctuelles ou cumulatives. Les informations OS concernent la machine cliente. Aucun changement SQL ni installation automatique.

Tests : `python3 -m unittest discover -s tests -v`. Intégration réelle à valider via CI.

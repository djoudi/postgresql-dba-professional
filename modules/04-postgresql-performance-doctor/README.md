# PostgreSQL Performance Doctor — Premium 1.0.0
Diagnostic en lecture seule, PostgreSQL 14–18 (cibles à valider), Python 3.9+, client psql. Ubuntu/Debian: `sudo apt install python3 postgresql-client`.

```bash
./doctor.sh
./doctor.sh --port 5432 --database postgres --output "$HOME/performance-reports"
python3 -m unittest discover -s tests -v
```
18 contrôles, rapports HTML/JSON privés. Aucun SQL applicatif collecté. Voir [guide](docs/GUIDE_FR.md) et [automatisation](docs/AUTOMATISATION.md). Code 0: collecte complète, 2: partielle, 1: échec. OBSERVE n'est pas un verdict de santé. UNKNOWN n'est pas un succès. Aucun réglage automatique.

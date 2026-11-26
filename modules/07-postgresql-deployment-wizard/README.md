# PostgreSQL Deployment Wizard Premium
Assistant CLI et interactif pour Ubuntu/Debian, PostgreSQL 14–18. Python 3 et Bash, sans dépendance Python externe.

## Démarrage
```bash
./wizard.sh detect
./wizard.sh install --version 18
sudo ./wizard.sh install --version 18 --apply
./wizard.sh create --version 18 --cluster formation --port 5435
sudo ./wizard.sh create --version 18 --cluster formation --port 5435 --apply
sudo ./wizard.sh configure --version 18 --cluster formation --ram 4096
sudo ./wizard.sh configure --version 18 --cluster formation --ram 4096 --fresh-lab --apply
./wizard.sh interactive
```
Sans `--apply`, aucune modification. Les opérations réelles demandent OUI. Installer préalablement Python 3 et configurer les dépôts APT approuvés. Le programme n'ajoute aucun dépôt ni clé. L'installation APT peut créer un cluster main automatiquement. Choisir un port libre et vérifier `pg_lsclusters`.

**Configuration réservée à un laboratoire neuf**: remplace pg_hba.conf, écoute localhost, peer sur socket, SCRAM sur TCP. Ne pas utiliser sur un serveur partagé ou de production existant. Le redémarrage interrompt les connexions. Les paramètres sont des estimations, pas une optimisation garantie. Voir docs/GUIDE_FR.md.

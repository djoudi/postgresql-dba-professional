# PostgreSQL DBA Professional Pack 2026 — Ultimate Edition

Collection de dix modules pédagogiques en français. PostgreSQL 14–18 ciblé; Ubuntu 22.04/24.04/26.04 selon module. **Version de formation, non certifiée production.**

## Démarrage
```bash
bash launcher.sh --check
bash launcher.sh
python3 tests/check_all.py
```
Le lanceur ne lance rien sans confirmation, ne demande pas sudo automatiquement et ne garantit pas le mode lecture seule des modules. Lire le README du module avant toute action. Utiliser une VM dédiée, des comptes limités, des sauvegardes testées et une console indépendante pour SSH. Les archives et rapports contiennent des informations sensibles.

## Documentation
- [Guide](docs/GUIDE_FR.md)
- [Fiches réflexes](docs/CHEAT_SHEETS.md)
- [100 questions et réponses](docs/ENTRETIENS_100.md)
- [Parcours 90 jours](docs/PARCOURS_90_JOURS.md)
- [Audit et limites](docs/AUDIT.md)
- [Résultats des tests](docs/RESULTATS_TESTS.txt)

## Publication GitHub
Créer un dépôt privé vide, puis depuis ce dossier : `git init`, `git add .`, `git commit -m "Ultimate Edition"`, `git branch -M main`, `git remote add origin URL_DU_DEPOT`, `git push -u origin main`. Vérifier les droits de redistribution avant publication publique. Aucun secret ni rapport réel ne doit être ajouté.

## Qualification RC2
Voir [qualification](docs/QUALIFICATION.md), [sécurité](SECURITY.md), [contribution](CONTRIBUTING.md) et [licence à valider](LICENSE-PENDING.md). Les tests CI et VM restent à exécuter.

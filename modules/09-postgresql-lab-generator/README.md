# PostgreSQL Lab Generator Premium — 1.0.0
Laboratoire DGPC fictif, PostgreSQL 14–18 (cibles), Python 3 et outils client PostgreSQL. Aucun accès aux données réelles nécessaire.

## Démarrage
```bash
sudo apt install python3 postgresql-client unzip
./lab.sh interactive
./lab.sh create --database lab_dgpc --rows 10000
./lab.sh create --database lab_dgpc --rows 10000 --apply
psql -X -d lab_dgpc -f corriges/01_sql.sql
```
Utiliser un rôle de formation CREATEDB sur une instance dédiée, jamais un superutilisateur de production. Le mode CLI est une simulation sans --apply. Une base existante n'est jamais écrasée. En cas d'échec après createdb, la base partielle est conservée pour diagnostic. Aucun DROP automatique. Les noms lab_ ne constituent pas une frontière de sécurité : isoler le serveur et le rôle.

## Parcours
Neuf ateliers : SQL, index, fonctions, procédures, triggers, transactions, verrous, CTE et sauvegarde/restauration. Les exercices et corrigés sont séparés. Les modifications des corrigés sont annulées par ROLLBACK. Voir docs/GUIDE_FR.md.

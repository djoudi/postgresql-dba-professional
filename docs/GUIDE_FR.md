# Guide d’exploitation

Installer Python 3, Bash et les clients PostgreSQL adaptés. Vérifier les dépendances avec `bash launcher.sh --check`. Ne jamais lancer le pack entier avec sudo.

## 01 — postgresql-dba-100-sql-scripts
Lire [README](../modules/01-postgresql-dba-100-sql-scripts/README.md). Bibliothèque : sélectionner un SQL, vérifier ses droits et son coût avant exécution.

## 02 — postgresql-backup-guardian
Lire [README](../modules/02-postgresql-backup-guardian/README.md). Entrée : `guardian.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 03 — postgresql-security-auditor
Lire [README](../modules/03-postgresql-security-auditor/README.md). Entrée : `auditor.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 04 — postgresql-performance-doctor
Lire [README](../modules/04-postgresql-performance-doctor/README.md). Entrée : `doctor.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 05 — postgresql-dba-emergency-handbook
Lire [README](../modules/05-postgresql-dba-emergency-handbook/README.md). Entrée : `scripts/diagnostic.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 06 — postgresql-health-report
Lire [README](../modules/06-postgresql-health-report/README.md). Entrée : `health.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 07 — postgresql-deployment-wizard
Lire [README](../modules/07-postgresql-deployment-wizard/README.md). Entrée : `wizard.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 08 — ubuntu-server-security-toolkit
Lire [README](../modules/08-ubuntu-server-security-toolkit/README.md). Entrée : `toolkit.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 09 — postgresql-lab-generator
Lire [README](../modules/09-postgresql-lab-generator/README.md). Entrée : `lab.sh`. Consulter les options et choisir explicitement le serveur et la base.

## 10 — postgresql-migration-assistant
Lire [README](../modules/10-postgresql-migration-assistant/README.md). Entrée : `migrate.sh`. Consulter les options et choisir explicitement le serveur et la base.

## Validation
Tester sur VM, documenter les versions, conserver les preuves et restaurer une sauvegarde avant toute intervention critique.

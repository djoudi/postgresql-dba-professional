# Correction
```bash
./lab.sh backup --database lab_dgpc --archive lab.dump --apply
sha256sum lab.dump > lab.dump.sha256
sha256sum -c lab.dump.sha256
./lab.sh restore --database lab_restore --archive lab.dump --apply
psql -d lab_dgpc -c 'SELECT count(*) FROM dgpc.interventions'
psql -d lab_restore -c 'SELECT count(*) FROM dgpc.interventions'
```
Adapter le port et le rôle. Comparer aussi les contraintes et les index avec \d dgpc.interventions. Les propriétaires et ACL ne sont pas restaurés. Le dump logique ne contient pas la chaîne WAL nécessaire au PITR.

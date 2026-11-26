# Automatisation
Installer le dossier dans un emplacement stable non modifiable par des tiers. Créer un répertoire privé pour les rapports. Exemple crontab du compte de monitoring (adapter les chemins):

```cron
0 7 * * * /usr/bin/flock -n /home/monitor/.doctor.lock /opt/performance-doctor/doctor.sh --port 5432 --database postgres --output /home/monitor/reports
```
Préparer la connexion non interactive et vérifier manuellement avant activation. Code 2 signifie collecte partielle. Surveiller les journaux et l'espace disque. La rétention est manuelle; aucun effacement automatique. Pour comparer les captures, vérifier la même cible et les dates de réinitialisation des statistiques. Les rapports contiennent des métadonnées sensibles.

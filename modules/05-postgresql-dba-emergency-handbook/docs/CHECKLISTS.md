# Checklists opérationnelles
## Avant intervention
- [ ] Identifier cluster, port, rôle primaire/standby et impact.
- [ ] Noter UTC, ticket, responsable, dernier changement.
- [ ] Préserver journaux et preuves dans un espace privé.
- [ ] Vérifier dernière sauvegarde restaurable et RPO/RTO.
- [ ] Obtenir autorisation et définir retour arrière.
## Pendant
- [ ] Une modification à la fois; journaliser commande et résultat.
- [ ] Ne jamais supprimer pg_wal, fichiers de données ou preuves.
- [ ] Escalader corruption, compromission, perte de données.
## Après
- [ ] Connexion, requêtes métier, droits, réplication, sauvegarde.
- [ ] Mesurer durée réelle et perte de données réelle.
- [ ] Informer parties prenantes; documenter cause et prévention.
## Fiche incident
Ticket / UTC début / UTC fin / cluster / impact / preuves / hypothèses / actions / validation / RPO réel / RTO réel / responsable / actions préventives.

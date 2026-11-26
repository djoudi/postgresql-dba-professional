# Plan de retour arrière
Avant migration: consigner responsables, fenêtre, RPO/RTO, endpoints, sauvegarde restaurable et critères d'abandon. Maintenir la source intacte et arrêter les écritures pendant la migration.
Avant bascule: en cas d'erreur, ne pas ouvrir la cible; conserver archive, rapports et base partielle. Rétablir les applications sur la source après validation. Corriger puis recommencer avec un nouveau nom de base et dossier.
Après bascule sans écriture cible: arrêter les applications, confirmer absence d'écritures, rétablir la configuration source, tester et rouvrir.
Après écritures cible: ne pas revenir aveuglément à la source. Isoler les deux systèmes, sauvegarder la cible, évaluer les transactions divergentes et organiser une réconciliation ou migration inverse validée. Décision métier explicite sur toute perte de données.
Checklist: [ ] sauvegarde testée; [ ] source gelée; [ ] archive vérifiée; [ ] données et droits validés; [ ] tests métier; [ ] accord de bascule; [ ] surveillance; [ ] clôture documentée.

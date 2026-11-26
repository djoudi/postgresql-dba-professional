# Sécurité et limites

Le compte postgres est privilégié : réserver l'outil aux administrateurs autorisés. Ne restaurer que des archives de confiance : une restauration peut exécuter du code SQL provenant de la source. Utiliser une VM isolée pour les essais. Les sommes SHA-256 détectent les altérations accidentelles, pas un attaquant capable de modifier les fichiers et les empreintes. Les archives ne sont pas chiffrées ; prévoir chiffrement au repos, copie hors site et stockage immuable. Ne pas exposer les journaux ou les archives.

Stratégie 3-2-1 : trois copies, deux supports, une hors site. Définir RPO/RTO selon le métier. Le dump logique ne fournit ni PITR, ni sauvegarde physique, ni réplication, ni garantie de durabilité après panne électrique. Pour PITR, déployer une solution éprouvée telle que pgBackRest ou Barman. La rotation automatique, Telegram et SMTP ne sont pas implémentés dans cette version. Les tests de restauration sont déclenchés manuellement.

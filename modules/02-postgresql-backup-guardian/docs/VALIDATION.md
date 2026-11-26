# Validation

Exécuter `bash tests/smoke.sh`. Ce test utilise des fichiers fictifs et vérifie le refus d'une archive altérée ; il ne valide pas PostgreSQL. Le workflow CI propose un test réel sur PostgreSQL 16 sous Ubuntu 24.04. Il doit être exécuté sur GitHub avant de déclarer sa réussite.

Recette sur VM : tester PostgreSQL 14, 16, 18 et Ubuntu 22.04, 24.04, 26.04 ; créer une base de test avec données, contraintes et routines ; sauvegarder, restaurer, comparer les résultats ; tester un port non standard, un cluster arrêté, une archive corrompue, un répertoire non autorisé, une destination existante, un manque d'espace et une tâche systemd. Consigner versions, durée, résultats et anomalies. Ne pas utiliser de données réelles dans les tests CI.

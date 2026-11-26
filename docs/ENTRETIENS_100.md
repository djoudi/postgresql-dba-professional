# 100 questions d’entretien DBA — réponses

### 001 — Architecture : Qu’est-ce qu’un cluster PostgreSQL ?
Une instance et son répertoire de données contenant plusieurs bases.

### 002 — Architecture : Quel est le rôle du WAL ?
Journaliser les modifications avant l’écriture des pages pour la récupération et la réplication.

### 003 — Architecture : Que fait un checkpoint ?
Il synchronise les pages modifiées selon le mécanisme de checkpoint et borne le travail de récupération.

### 004 — Architecture : Qu’est-ce que MVCC ?
Des versions de lignes permettent des lectures cohérentes malgré les écritures concurrentes.

### 005 — Architecture : Que contient shared_buffers ?
Le cache de pages géré par PostgreSQL.

### 006 — Architecture : Quel est le rôle du processus backend ?
Exécuter les requêtes d’une connexion cliente.

### 007 — Architecture : Que signifie ACID ?
Atomicité, cohérence, isolation et durabilité.

### 008 — Architecture : Base ou schéma ?
Une base est une frontière de connexion; un schéma organise ses objets.

### 009 — Architecture : Pourquoi un tablespace ?
Placer des objets sur un emplacement de stockage distinct.

### 010 — Architecture : Que fait le planificateur ?
Il estime les coûts et choisit un plan d’exécution.

### 011 — SQL : INNER JOIN ou LEFT JOIN ?
INNER conserve les correspondances; LEFT conserve aussi les lignes de gauche sans correspondance.

### 012 — SQL : WHERE ou HAVING ?
WHERE filtre avant agrégation; HAVING filtre les groupes.

### 013 — SQL : COUNT(*) ou COUNT(colonne) ?
Le premier compte les lignes; le second ignore les NULL.

### 014 — SQL : Que fait une CTE ?
Elle nomme un résultat intermédiaire pour structurer une requête.

### 015 — SQL : À quoi sert une fenêtre SQL ?
Calculer sur un ensemble de lignes sans les réduire à une ligne par groupe.

### 016 — SQL : Pourquoi une clé étrangère ?
Garantir l’intégrité référentielle.

### 017 — SQL : Pourquoi UNIQUE ?
Empêcher les doublons selon les règles de NULL de la contrainte.

### 018 — SQL : Vue ou vue matérialisée ?
La première exécute sa définition; la seconde stocke un résultat à rafraîchir.

### 019 — SQL : Comment tester NULL ?
IS NULL, jamais une égalité ordinaire avec NULL.

### 020 — SQL : Que fait ON CONFLICT ?
Gérer un conflit d’unicité par une action explicite.

### 021 — Administration : Comment lister les clusters Ubuntu ?
pg_lsclusters, fourni par postgresql-common.

### 022 — Administration : Comment connaître la version serveur ?
SHOW server_version; ou SELECT version().

### 023 — Administration : Comment trouver le fichier de configuration ?
SHOW config_file; et SHOW hba_file;.

### 024 — Administration : Reload ou restart ?
Reload relit les paramètres rechargeables; restart arrête puis relance le service.

### 025 — Administration : Comment voir les paramètres en attente ?
Interroger pg_settings WHERE pending_restart.

### 026 — Administration : Que fait ANALYZE ?
Met à jour les statistiques utilisées par le planificateur.

### 027 — Administration : Que fait VACUUM ?
Rend réutilisable l’espace des versions mortes et contribue au gel des XID.

### 028 — Administration : Pourquoi éviter VACUUM FULL systématique ?
Il réécrit la table, exige de l’espace et prend un verrou exclusif.

### 029 — Administration : Comment voir les tailles ?
pg_database_size et pg_total_relation_size.

### 030 — Administration : Comment vérifier la disponibilité ?
pg_isready puis une vraie connexion SQL; le premier ne valide pas les droits.

### 031 — Sécurité : Que fait pg_hba.conf ?
Définit les règles d’authentification, évaluées dans l’ordre jusqu’à la première correspondance.

### 032 — Sécurité : Qu’est-ce que SCRAM ?
Un mécanisme d’authentification par défi-réponse fondé sur un secret dérivé.

### 033 — Sécurité : Pourquoi éviter trust ?
Il autorise la connexion sans vérification du mot de passe pour la règle correspondante.

### 034 — Sécurité : Que fait peer ?
Vérifie l’identité du compte OS pour une connexion locale.

### 035 — Sécurité : LOGIN et NOLOGIN ?
LOGIN autorise une connexion; NOLOGIN convient aux rôles de groupe.

### 036 — Sécurité : Pourquoi pg_monitor ?
Accorder des droits de surveillance sans superutilisateur, avec visibilité néanmoins sensible.

### 037 — Sécurité : USAGE sur schéma suffit-il ?
Non, il faut aussi les droits sur les objets.

### 038 — Sécurité : Que fait verify-full ?
Vérifie la chaîne de confiance TLS et le nom du serveur.

### 039 — Sécurité : Risque SECURITY DEFINER ?
Exécution avec les droits du propriétaire; sécuriser search_path et EXECUTE.

### 040 — Sécurité : Que fait RLS ?
Filtre les lignes selon des politiques; tester les exemptions des propriétaires et rôles privilégiés.

### 041 — Performance : EXPLAIN ou EXPLAIN ANALYZE ?
Le second exécute réellement la requête; attention aux écritures et au coût.

### 042 — Performance : Pourquoi BUFFERS ?
Observer les accès aux blocs, hits et lectures notamment.

### 043 — Performance : Quand un scan séquentiel est-il pertinent ?
Quand une grande fraction de la table est nécessaire ou que la table est petite.

### 044 — Performance : Qu’est-ce qu’un index partiel ?
Un index limité aux lignes satisfaisant un prédicat.

### 045 — Performance : Pourquoi un index inutilisé ne doit-il pas être supprimé immédiatement ?
Les statistiques peuvent être récentes ou le besoin rare mais critique.

### 046 — Performance : Que signifie work_mem ?
Budget de base par opération de tri ou hachage, multipliable par requête et travailleurs.

### 047 — Performance : Que signifie effective_cache_size ?
Estimation du cache accessible au planificateur, pas une allocation.

### 048 — Performance : Comment trouver les requêtes coûteuses ?
pg_stat_statements si activé; examiner temps cumulé, moyen et appels.

### 049 — Performance : Un cache hit élevé garantit-il la vitesse ?
Non, CPU, verrous et autres coûts peuvent dominer.

### 050 — Performance : Pourquoi comparer estimations et lignes réelles ?
Détecter des erreurs de cardinalité qui influencent le choix du plan.

### 051 — Transactions : Que fait BEGIN ?
Ouvre une transaction explicite.

### 052 — Transactions : Que fait COMMIT ?
Valide les modifications de la transaction.

### 053 — Transactions : Que fait ROLLBACK ?
Annule les modifications transactionnelles non validées.

### 054 — Transactions : Que fait SAVEPOINT ?
Crée un point de retour partiel dans la transaction.

### 055 — Transactions : Isolation par défaut ?
READ COMMITTED, avec un snapshot par instruction.

### 056 — Transactions : Qu’est-ce qu’un deadlock ?
Un cycle d’attentes; PostgreSQL annule une transaction pour le résoudre.

### 057 — Transactions : Comment identifier un bloqueur ?
pg_blocking_pids(pid) et pg_stat_activity.

### 058 — Transactions : Pourquoi idle in transaction est-il risqué ?
Il peut retenir des verrous et empêcher le nettoyage de versions.

### 059 — Transactions : cancel ou terminate ?
Cancel annule la requête; terminate ferme la session et annule sa transaction ouverte.

### 060 — Transactions : Que faire après une erreur de sérialisation ?
Rejouer la transaction entière selon une stratégie bornée de retry.

### 061 — Sauvegarde : pg_dump sauvegarde quoi ?
Une base logique, pas le cluster complet ni tous les rôles.

### 062 — Sauvegarde : Pourquoi le format custom ?
Il permet pg_restore et la sélection d’objets.

### 063 — Sauvegarde : Que fait pg_dumpall --globals-only ?
Exporte les objets globaux; protéger les secrets et examiner les rôles.

### 064 — Sauvegarde : Qu’est-ce que RPO ?
Perte de données maximale acceptable exprimée en temps.

### 065 — Sauvegarde : Qu’est-ce que RTO ?
Durée maximale acceptable de rétablissement.

### 066 — Sauvegarde : SHA-256 suffit-il ?
Non, il vérifie l’intégrité par rapport à une empreinte fiable, pas la restaurabilité.

### 067 — Sauvegarde : Pourquoi tester une restauration ?
Prouver que l’archive, les dépendances et les procédures fonctionnent.

### 068 — Sauvegarde : Qu’exige PITR ?
Une sauvegarde physique compatible et une chaîne WAL complète jusqu’à la cible.

### 069 — Sauvegarde : Pourquoi une copie hors site ?
Réduire le risque de perte simultanée du serveur et des sauvegardes.

### 070 — Sauvegarde : Pourquoi ne pas effacer pg_wal ?
Cela peut rendre le cluster irrécupérable ou incohérent.

### 071 — Réplication : Physique ou logique ?
Physique réplique les changements de stockage via WAL; logique publie des changements de données.

### 072 — Réplication : Que fait un slot ?
Retient les ressources nécessaires au consommateur; surveiller la croissance WAL.

### 073 — Réplication : Comment voir les réplicas connectés ?
pg_stat_replication sur le primaire.

### 074 — Réplication : Comment détecter un standby ?
SELECT pg_is_in_recovery().

### 075 — Réplication : Réplication synchrone ou asynchrone ?
La synchrone attend les confirmations configurées; l’asynchrone peut perdre des transactions lors d’une panne.

### 076 — Réplication : Qu’est-ce que le lag ?
Retard de réception, écriture, flush ou replay; distinguer octets et temps.

### 077 — Réplication : Qu’est-ce que split-brain ?
Deux nœuds acceptent des écritures incompatibles comme primaires.

### 078 — Réplication : Une réplication remplace-t-elle une sauvegarde ?
Non, les suppressions et erreurs peuvent être répliquées.

### 079 — Réplication : Que vérifier avant promotion ?
Isoler l’ancien primaire, évaluer le retard et obtenir l’autorisation.

### 080 — Réplication : La réplication logique copie-t-elle automatiquement le DDL ?
Non, gérer les changements de schéma et les séquences séparément.

### 081 — Incidents : Premier réflexe si le service ne démarre pas ?
Identifier le cluster, lire les journaux et vérifier stockage et configuration.

### 082 — Incidents : Que vérifier si connexion refusée ?
Adresse, port, écoute, service et pare-feu.

### 083 — Incidents : Que faire si disque plein ?
Identifier le volume, limiter la croissance et étendre/libérer uniquement des fichiers sûrs.

### 084 — Incidents : Que faire si corruption suspectée ?
Préserver les preuves, isoler et restaurer une copie saine; éviter les réparations improvisées.

### 085 — Incidents : Comment diagnostiquer OOM ?
Consulter les journaux noyau, mémoire, connexions et paramètres.

### 086 — Incidents : Que faire si trop de connexions ?
Identifier les clients, limiter la pression et envisager un pool; ne pas augmenter aveuglément la limite.

### 087 — Incidents : Comment suivre autovacuum ?
pg_stat_user_tables, pg_stat_progress_vacuum et journaux.

### 088 — Incidents : Pourquoi surveiller age(datfrozenxid) ?
Prévenir les risques liés au wraparound des identifiants de transactions.

### 089 — Incidents : Que faire après suppression accidentelle ?
Suspendre les écritures pertinentes, préserver les sauvegardes et restaurer en isolation.

### 090 — Incidents : Quand clore un incident ?
Après validation technique et métier, documentation et actions préventives.

### 091 — Migration : Pourquoi utiliser un pg_dump récent ?
Il doit prendre en charge la version source; utiliser celui de la cible pour un upgrade logique.

### 092 — Migration : Pourquoi une base cible neuve ?
Éviter collisions et écrasement d’objets existants.

### 093 — Migration : Pourquoi inventorier les extensions ?
Les bibliothèques et versions compatibles doivent être disponibles sur la cible.

### 094 — Migration : Pourquoi vérifier collation et locale ?
Elles influencent tris, comparaisons et index.

### 095 — Migration : Que fait --no-owner ?
Ne restaure pas les propriétaires originaux; reconstruire les droits.

### 096 — Migration : Pourquoi arrêter les écritures ?
Éviter des modifications non transférées entre export et bascule.

### 097 — Migration : Les comptages égaux suffisent-ils ?
Non, comparer aussi contenu, contraintes, séquences, droits et tests métier.

### 098 — Migration : Qu’est-ce que pg_upgrade ?
Un outil de mise à niveau majeure utilisant les clusters physiques compatibles.

### 099 — Migration : Quand revenir à la source ?
Avant écritures cible, après validation; sinon réconcilier les nouvelles transactions.

### 100 — Migration : Que faire après restauration ?
Analyser les tables, vérifier droits, séquences, plans et application.
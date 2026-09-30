> Référence du dépôt historique, conservée pour l’étude. Les anciens lancements, secrets, certificats et migrations cités ne font pas partie du livrable. Utiliser uniquement `docker-compose.local.yml`, `config.settings_local` et https://localhost:8443.

# My Climbing List — Recommandations pour la refonte

Document prospectif établi le 10 septembre 2026 après vérification statique du dépôt et relecture de `MCL_ANALYSE_TECHNIQUE.md`. Il complète [la notice de reprise](MCL_NOTICE_REPRISE.md), qui décrit les comportements actuels et le registre de règles R01–R24. Les choix ci-dessous sont des propositions pour la refonte, et non des composants déjà présents. Aucune modification applicative ni opération sur une base n'a été effectuée.

Convention : `applications/` désigne `app/src/applications/`. Le périmètre effectivement utilisé, la volumétrie, les moyens de l'équipe, les garanties du flux externe et les objectifs de disponibilité doivent encore être établis. Les anomalies du POC servent à définir des exigences et des tests ; elles ne deviennent pas le règlement du nouveau produit.

## 1. Principes directeurs

1. **Les règles appartiennent au métier, pas aux écrans.** Un top valide, l'éligibilité à une compétition et le calcul d'un projet doivent être définis une fois, appelables depuis web, API et jobs, et testables sans navigateur.
2. **Chaque donnée a une source de vérité identifiée.** Le catalogue vient d'une source externe contrôlée ; la pratique vient du grimpeur ; un résultat sportif provient d'un règlement et d'un ensemble de performances ; un cache n'est jamais la source d'un calcul.
3. **Distinguer faits, décisions et dérivés.** Essais et dates sont des faits déclarés ; masquer un projet ou accorder un suivi sont des décisions ; Elo, affiliation calculée et classements sont des dérivés. On ne les migre ni ne les invalide de la même façon.
4. **Les permissions sont explicites et liées aux objets.** Le rôle professionnel d'une personne ne découle ni de sa favorite ni de l'URL appelée. Le consentement au suivi ne s'infère pas d'une simple appartenance à une salle.
5. **Le passé reste interprétable.** Préserver IDs, provenance, valeurs importées et versions des règles ; une correction doit expliquer pourquoi un calcul historique change.
6. **L'environnement est reproductible.** Un développeur doit travailler avec PostgreSQL et un jeu synthétique, sans réseau ni identifiants de production. L'OS de sa machine ne détermine pas le mode applicatif.
7. **Le déploiement est prévisible.** Démarrer le web ne migre pas une base, ne retire pas d'inscriptions et ne télécharge pas le topo. Chaque opération a une responsabilité, une procédure et un résultat observable.
8. **La documentation et les tests font partie de la livraison.** Une règle modifiée implique exemple, test, version et note de décision. Une nouvelle dépendance implique propriétaire et procédure de diagnostic.

Ces principes répondent notamment à `core/utils/views/session.py`, `staff_admin/utils/elo_engine.py`, `contest/utils/scoring.py`, `event/permissions.py`, `config/settings.py` et `app/entrypoint.sh`.

## 2. Architecture cible

**Choix proposé : monolithe Django modulaire, PostgreSQL et API REST, avec un web responsive puis une PWA.** Il conserve une pile cohérente avec le domaine et limite le nombre de systèmes à exploiter. Aucun besoin observé ne justifie des microservices : les principales opérations exigent au contraire des transactions communes entre pratique, catalogue et inscriptions.

```text
Web responsive / PWA                  Future application iOS / Android
           └──────────────── API REST ─────────────────┘
                                  │
                  Authentification + permissions objet
                                  │
                     Cas d'usage métier Django
            identité | salles | catalogue | pratique
             progression | compétitions | statistiques
                                  │
                  PostgreSQL + journal des changements
                                  │
               données dérivées / résultats publiés

Planificateur unique → exécuteur de jobs → mêmes cas d'usage
                       imports, recalculs, emails
Observabilité : erreurs API + exécutions jobs + contrôles de cohérence
```

| Composant | Choix et justification | Condition / limite |
|---|---|---|
| Backend | Applications Django par domaine, services de cas d'usage, requêtes dédiées aux lectures | Ne pas recréer un `core` absorbant tout le produit |
| API REST | Contrat commun pour pratique, catalogue, projets, niveaux et compétitions | Un JSON qui transporte du HTML ne constitue pas ce contrat |
| PostgreSQL | Persistance, contraintes, transactions, requêtes analytiques proportionnées | Version soutenue et stratégie de sauvegarde à fixer à l'implémentation |
| Frontend web | Responsive, un client principal ; templates possibles pour certains back-offices | Choisir un framework frontend séparé seulement si les parcours et compétences le justifient |
| PWA | Installation, consultation du topo sélectionné, brouillons clairement identifiés | Écritures hors ligne seulement après définition du protocole de synchronisation |
| iOS/Android | Consommateur futur de la même API et des mêmes règles | Ne pas décider aujourd'hui du framework mobile sans cadrage des usages natifs |
| Jobs | Processus séparé du web, même image/version métier, planificateur unique | Un ordonnanceur et des commandes robustes peuvent suffire au départ ; une file devient utile pour retries, emails et recalculs à la demande |
| Cache | Données dérivées datées et invalidables ; stockage partagé seulement si nécessaire | Commencer sans cache métier là où les requêtes indexées suffisent |

Organiser les points d'entrée d'exploitation dans `scripts/` (courts, idéalement moins de 150 lignes) et la logique réutilisable dans `lib/`, avec sous-domaines explicites. Dans Django, les modèles, vues, serializers et migrations restent dans leurs applications conventionnelles. Exemple : `scripts/import_catalogue.py` appelle `lib/catalogue/importer.py` ; une commande Django peut être un adaptateur très mince du même service. Ne pas faire de `lib/` un nouveau fourre-tout.

Pour la pratique, une transaction enregistre une séance cohérente. Les notifications ou recalculs sont déclenchés après validation de la transaction ; si leur livraison doit résister à un crash, une petite table de tâches/outbox transactionnelle permet de les reprendre. La documentation Django décrit `atomic()` et les actions après commit : [transactions Django](https://docs.djangoproject.com/en/dev/topics/db/transactions/). La version exacte du framework et de ses bibliothèques sera choisie et vérifiée lors de l'implémentation, sans reconduire mécaniquement `requirements.txt`.

## 3. Découpage des domaines

| Domaine | Responsabilités | Données possédées / interfaces |
|---|---|---|
| Identité et permissions | Comptes, authentification, rôles nominatifs, consentements, préférences | Compte, profil, attribution de rôle, autorisation de suivi ; service `peut_consulter_pratique` |
| Salles | Référentiel des sites, secteurs/relais, capacités, fuseaux, plans | Salle, emplacement, capacités historisées ; aucune logique d'authentification |
| Catalogue d'ouvertures | Identités externes, import, normalisation, versions, activation/retrait | Ouverture, version descriptive, mapping source, lot d'import |
| Pratique | Séances, activité sur une ouverture, essais/réalisations et corrections, objectifs personnels | Séance, pratique agrégée ou tentatives, projet ; événements de changement |
| Progression | Éligibilité, calcul de niveau, état du moteur, tendances et explications | Résultats par discipline/date/version ; lit des faits de pratique normalisés |
| Compétitions | Inscriptions, paiements validés, équipes, créneaux, règlements, performances, publication | Compétition et déclinaisons de règlement ; identités participantes avec compte facultatif |
| Statistiques et publication | Indicateurs utilisateur/staff/direction, Alti Ligue, exports | Projections datées, définitions d'indicateurs, snapshots publiés ; pas de mutation implicite des faits |

Les interfaces peuvent être de simples fonctions Python et objets de résultat dans le même processus. Aucun bus distribué n'est nécessaire pour établir ces frontières. Le catalogue ne dépend pas du staff ; progression ne dépend pas de Plotly ; les statistiques ne modifient pas une inscription pendant une lecture. Les trois règlements sportifs peuvent partager inscriptions/créneaux/publication sans partager une formule artificiellement universelle.

Sources du découpage : `custom_auth/models/salle.py` et `profile.py`, `core/models/`, `staff_admin/models/climber_level_daily.py`, `contest/models/`, `event/models/`, `route_event/models/`, `dir_admin/management/commands/`.

## 4. Modèle de données à améliorer

### Séance et pratique

Créer une **Séance** avec ID stable, utilisateur, salle, date locale, fuseau, et éventuellement début/fin si le produit en a réellement besoin. La discipline peut être portée par les activités : une visite mixte est possible conceptuellement. Autoriser deux séances le même jour ; décider comment l'interface les distingue. Ne jamais utiliser uniquement utilisateur/date/salle comme identité de séance future.

Créer une **Pratique d'ouverture** liée à la séance et à l'ouverture/version utilisée. Deux approches doivent être arbitrées :

- Si l'utilisateur saisit des totaux, conserver des compteurs agrégés par mode avec contraintes. C'est fidèle au besoin de saisie rapide et aux données historiques.
- Si le produit demande un ordre de tentatives, ajouter une table Tentative avec mode, issue et horodatage facultatif. Ne pas fabriquer des heures ou une chronologie sportive à partir des anciens compteurs.

Un top est une réussite parmi les essais ; `0 ≤ tops ≤ essais`. Le bloc ne possède pas de canal tête. Un flash est une propriété d'une réussite selon un règlement de première tentative, pas un booléen libre sans réalisation associée. Pour le passé agrégé, conserver les drapeaux d'origine et leur provenance, même si leur validation est impossible.

Les mises à jour de séance sont atomiques, avec contrôle de version et stratégie de conflit. Déplacer une séance sur une date occupée ne doit jamais supprimer les autres séances. Une suppression doit créer un signal d'invalidation et rester traçable selon la politique de conservation. Référence du problème : `core/utils/views/session.py`.

### Catalogue et emplacements

Créer des IDs internes indépendants des IDs Altissimo. Une contrainte unique sur `(source, identifiant_externe)` empêche le doublonnage d'import. Relier chaque ouverture à un emplacement typé voie/bloc, lui-même rattaché à la salle ; séparer secteur et relais si leurs attributs divergent réellement.

Versionner les propriétés qui influencent les calculs : cotation, discipline, salle/emplacement, capacités tête et statut. Déterminer avec le métier si une correction de cotation doit corriger tout le passé ou seulement les nouvelles réalisations. Dans les deux cas, conserver l'ancienne valeur et la décision. Une donnée inconnue reste inconnue, sans transformation silencieuse en difficulté valide.

Retrait logique d'une ouverture et protection des références historiques sont nécessaires ; la suppression physique doit être un cas d'usage explicite. Les suppressions de données personnelles ont leur propre politique : la suppression logique n'est pas un prétexte à conserver indéfiniment un compte supprimé.

### Rôles, projets et calculs

Remplacer les champs détournés du profil par des **attributions de rôle par salle**, avec début/fin et auteur. La direction possède un droit explicite multi-salles sans nécessiter automatiquement tous les droits du superutilisateur technique. Le partage de pratique possède son propre état actif/révoqué.

Créer Projet avec utilisateur, ouverture, objectif (par exemple top tête), statut et choix de visibilité. Séparer détection automatique d'un candidat et décision de masquage. Un nouvel essai ne réinitialise cette décision que si la règle a été approuvée.

Stocker les niveaux avec version du moteur, date de référence, provenance des entrées et état complet nécessaire à la reprise. Un simple nombre Elo est insuffisant pour continuer le moteur actuel, car il manque le plafond d'échecs par ouverture. Garder l'option d'un recalcul complet avant d'optimiser l'incrémental.

### Compétitions

Conserver une version de règlement et un catalogue sportif figé à la clôture. Les performances restent typées : top/zone pour bloc, prise/« + » pour voie, top/zone/dégaine pour les Contest qui l'exigent. Définir contraintes d'unicité, cohérence salle/discipline/événement et capacité sous concurrence.

Une phase horaire n'est pas automatiquement un tour sportif. Si finales ou qualifications indépendantes sont nécessaires, modéliser des rounds avec leurs propres voies, performances, populations et règles de qualification. Le marqueur des six duos mixtes ne suffit pas à décrire ce cycle.

## 5. API et applications mobiles

L'API expose des ressources métier stables : salles/emplacements, ouvertures, séances/pratiques, projets, progression, compétitions/inscriptions/performances et résultats publiés. Les clients obtiennent des données structurées et des capacités autorisées ; ils choisissent leur présentation. Les exports appellent les mêmes services de classement que l'API.

Prévoir un contrat documenté, pagination, filtres, ordre stable, erreurs par champ et codes d'erreur durables. Séparer date sportive, instant technique et fuseau. Pour un changement incompatible de contrat, conserver une période de compatibilité avec les versions mobiles encore utilisées. Une version de l'API ne remplace pas la version d'un règlement sportif.

Pour les écritures :

- Identifiant de requête/idempotence pour qu'un retry mobile ne crée pas deux séances.
- Contrôle de version pour refuser ou résoudre explicitement deux modifications concurrentes.
- Vérification serveur de l'acteur, de la salle, de l'ouverture, des compteurs et du règlement avant toute mutation.
- Publication d'un lot de performances de façon atomique, avec retour explicite des erreurs.
- Aucune écriture dans les GET : initialisation des scores et préparation des projections dans des cas d'usage dédiés.

Le web same-origin peut utiliser des sessions sécurisées et CSRF ; le mobile aura une authentification adaptée avec révocation et stockage sécurisé. Le mécanisme exact sera choisi lors de la conception sécurité, sans réutiliser des liens permanents d'événement comme authentification générale.

PWA : commencer par topo consultable et brouillon non envoyé. Afficher clairement « enregistré sur cet appareil » et « enregistré sur le serveur ». Si la synchronisation est ajoutée, spécifier IDs locaux, retries, conflits, clôture de compétition pendant la déconnexion et retrait d'une ouverture entre saisie et envoi. Une performance tardive ne devient pas recevable parce qu'elle a été saisie hors ligne. Isoler les données par compte, limiter la durée de cache et purger même si le logout réseau échoue.

Sources des limites : `core/refresh_views/`, `contest/views/ranking.py`, `contest/views/submit_result.py`, `app/src/static/base/pwa/config/sw/`.

## 6. Tests

La priorité est de capturer les règles et les anomalies avant de remplacer les traitements. Constituer des données synthétiques lisibles et des résultats attendus validés avec le responsable métier. Garder deux catégories explicites : **test de caractérisation du POC** et **test de comportement cible**. Lorsqu'une anomalie est corrigée, son ancien résultat reste documenté comme écart accepté, pas comme test cible obligatoire.

Quatre niveaux suffisent au départ : fonctions métier pures pour formules et décisions ; intégration PostgreSQL pour contraintes/transactions/concurrence ; API pour permissions et contrats ; quelques parcours navigateur critiques pour la saisie et la PWA. Les tests de migration utilisent une copie anonymisée ou des fixtures représentatives et vérifient les correspondances, pas seulement les totaux globaux.

Voici **28 cas de référence** directement motivés par le code actuel. Rxx renvoie au registre de la notice ; le résultat proposé est à approuver lorsqu'un arbitrage est mentionné.

| Nº | Scénario | Résultat à contrôler et nature |
|---|---|---|
| 01 | Bloc dont le numéro de secteur existe aussi dans les relais tête | Aucun canal ni projet tête ; corrige R01, `projects.py` |
| 02 | 3 essais, 1 top dans un mode ; POST avec tops > essais ou négatifs | 2 échecs pour le premier ; rejet atomique des autres ; R02, `session.py` |
| 03 | Premier essai réussi, puis répétitions ; flash déclaré sans top | Bonus sur la réussite éligible uniquement ; rejet sans top ; R03/R10 |
| 04 | Moulinette antérieure puis première réussite en tête | Arbitrage explicite du flash tête et impact Elo ; ne pas déduire la réponse du seul JS |
| 05 | Top moulinette sur voie tête, puis top tête | Projet conservé puis terminé, topo déjà réussi dès moulinette ; R04 |
| 06 | Projet masqué, nouvelle activité un autre jour, deux lignes même date | Visibilité conforme à la politique approuvée, ordre déterministe ; R05 |
| 07 | Ouverture retirée puis réactivée avec le même ID source | Une seule identité ; carnet conservé ; topo/projet cohérents ; R06 |
| 08 | Cotations 4+, 5a+, inconnue et libellé commençant par 5 mais invalide | Pas de crash ; exclusions et regroupements approuvés ; R07 |
| 09 | Plusieurs tops sur une ouverture, dans les deux modes | Diversité = une ouverture, volume = total réel ; priorité tête de l'ancien indicateur caractérisée ; R08 |
| 10 | Flash moulinette un jour, top tête un autre jour | Distinguer « flash et tête existent » de « flash en tête » ; `logbook.py` |
| 11 | 11 puis 12 lignes réussies, dont répétitions de la même ouverture | Seuil d'amorçage caractérisé ; choix cible entre lignes/distincts/tops validé ; R09 |
| 12 | État Elo fixé, réussite normale/flash/tête/flash tête | Formule et coefficients R10 calculés indépendamment, précision et ordre convenus |
| 13 | Quatre échecs sur la même ouverture répartis sur plusieurs jours | Plafond validé identique en calcul complet et incrémental ; R11 |
| 14 | Modification, suppression, déplacement d'une ancienne séance, puis correction de cotation | Invalidation depuis la bonne date, résultat incrémental = recalcul complet ; R12 |
| 15 | Déplacement vers une date où cette ouverture est déjà pratiquée ; ligne mise à zéro | Pas de perte d'autre séance ; décision explicite sur suppression ; `session.py` |
| 16 | Double envoi simultané d'une séance | Une seule mutation logique, pas de doublon, contrôle de conflit si contenus différents |
| 17 | CSV valide rejoué deux fois, IDs dupliqués et salle inconnue | Import idempotent ; rapport des rejets ; aucune duplication ni changement de référence |
| 18 | CSV en-tête seul, tronqué, HTML 200, erreur réseau et lot massivement réducteur | Lot rejeté ou mis en attente ; aucune désactivation globale ; `csv.py`, `deactivate_old_entries.py` |
| 19 | Staff salle A demande calendrier d'un grimpeur autorisant B ; consentement révoqué | Refus via URL directe, API et route localisée ; R24 |
| 20 | Favorite du staff changée ; utilisateur standard appelle un endpoint staff/direction | Aucun droit nouveau ; politiques objet et rôle appliquées indépendamment de l'URL |
| 21 | Contest gratuit pending/refused et payant pending/accepted ; voie extérieure ; contest clos | Éligibilité selon statut ; rejet des écritures hors catalogue/fenêtre ; R13 |
| 22 | Permanent : pratique avant début, saisie après fin, ouverture retirée | Ancienne règle `created_at` caractérisée ; choix cible de période et gel validé ; R14 |
| 23 | Deux grimpeurs topent la même ouverture en 1000 points ; compte non éligible en plus | 500 chacun si deux éligibles selon règlement cible ; dénominateur partagé par écran/export/report ; R15/R17 |
| 24 | Équipe avec deux toppers et un adversaire ; reprise de score précédent | Formule actuelle équipe : 2×1000/(1+1)=1000 ; valider héritage et permanent ; score initial figé hors GET ; R16/R17 |
| 25 | Scores égaux, zones/dégaines différentes, fractions avant troncature | Rangs et départages approuvés, précision cohérente ; R15/R18 |
| 26 | Event : deux derniers inscrits concurrents sur une place, top sans zone, paiement absent, borne horaire, égalité à la sixième équipe mixte | Capacité non dépassée, invariants et clôture respectés, qualification approuvée ; R18/R19/R21 |
| 27 | RouteEvent : prises 10/10+/absence, ex æquo, changement filtre genre/phase | + = 0,5 ; rangs moyens, moyenne géométrique et population validés ; tester arrondi, compétition sans voie et zéro+ ; R20 |
| 28 | Alti Ligue : activité uniquement dans l'autre discipline/future, candidats sans salle dans les 100 premiers, égalité Elo | Éligibilité, limite, affiliation et départage documentés ; aucune dépendance à l'ordre DB implicite ; R22 |

En complément transversal : tester la purge de cache entre deux comptes, une reprise après interruption de job et la restauration de sauvegarde. Pour les indicateurs direction, utiliser un jeu où un utilisateur change de salle : vérifier que la métrique cible n'attribue pas automatiquement tout son passé à sa dernière salle.

Ne pas limiter l'oracle à « ancien résultat = nouveau résultat » : les deux peuvent partager la même erreur. Les scores et invariants doivent être calculés indépendamment sur de petits exemples. La CI exécute les tests sur PostgreSQL isolé sans variables de production ni appels au flux réel. Des fixtures importées ne doivent contenir aucun accès événement exploitable.

## 7. Sécurité

Transformer les constats de la notice en exigences vérifiables :

| Constat | Exigence cible et preuve attendue |
|---|---|
| Secrets dans la copie, fichiers privés et configuration | Renouvellement/révocation des accès concernés ; secrets injectés à l'exécution ; scan dépôt, historique accessible et image ; exemples avec valeurs factices uniquement |
| Saisie Contest insuffisamment contrôlée | Service de soumission vérifiant acteur, inscription, paiement attendu, catalogue, fenêtre et contenu ; tests négatifs API |
| Calendrier sans vérification de suivi | Autorisation objet commune aux listes, détails, exports et API ; tests avant/après révocation |
| Droits par favorite/salle voie/préfixe URL | Rôles nominatifs par salle, refus par défaut, direction distincte du superuser ; matrice de droits validée |
| Compteurs et relations insuffisamment contraints | Validation applicative et contraintes DB pour les invariants locaux ; contrôles transactionnels pour relations et capacités |
| Liens événement porteurs et persistants | Périmètre limité, révocation/réémission et expiration définies ; absence dans logs, analytics, exports ordinaires et rapports d'erreur |
| Cache authentifié | Cloisonnement par utilisateur, purge, durée limitée, données sensibles exclues du cache non nécessaire |
| Suppression et emails couplés | Suppression maîtrisée ; confirmation asynchrone après commit, erreur SMTP sans restauration implicite du compte ni faux message d'échec de suppression |
| Images/runtime peu reproductibles | Versions maintenues, dépendances et images contrôlées, exécution sans privilèges excessifs, séparation rôle DB applicatif/migration |

Revoir les paramètres de production, HTTPS, cookies et remontées d'erreurs avant ouverture. La [checklist officielle Django](https://docs.djangoproject.com/en/dev/howto/deployment/checklist/) sert de contrôle technique de base ; les permissions par salle et règles sportives restent propres à MCL et nécessitent leurs tests. Faire valider conservation des données, publication des identités et modalités de partage par les responsables compétents ; ce document ne fixe pas une durée légale par défaut.

## 8. Déploiement

| Étape | Responsabilité proposée | Condition de réussite |
|---|---|---|
| Build | Installer dépendances figées, compiler/collecter les statiques, exécuter contrôles, produire une image immuable | Aucun accès ni secret de production pendant le build |
| Préparation | Vérifier sauvegarde restaurable, compatibilité schéma et version, capacité disponible | Identifiant de livraison et plan de retour documentés |
| Migration | Job unique, compte DB dédié, supervision et arrêt sur erreur | Migration rejouable/testée sur données représentatives ; aucune restauration utilisateur ponctuelle cachée |
| Déploiement web | Démarrer la version préparée et vérifier readiness/parcours minimal | Le démarrage n'importe ni ne nettoie les données |
| Imports | Job explicite, instantané validé, verrou d'exécution, journal et bilan | Lot appliqué une seule fois ; rejet préserve le catalogue courant |
| Planification | Un planificateur, jobs séparés avec dépendances de réussite | Elo terminé avant publication Alti Ligue ; absence d'exécution concurrente non maîtrisée |
| Serveur web | Reverse proxy, TLS, statiques et logs d'accès expurgés | Santé observée, renouvellement surveillé, bootstrap TLS documenté |

Pour les évolutions de schéma, préférer ajout compatible → migration des données → adoption du nouveau champ → retrait ultérieur. Éviter une migration longue et destructrice couplée au redémarrage de chaque worker. La collecte des statiques doit pouvoir fonctionner avec une configuration de build sans DB de production ; utiliser une version de livraison stable pour les caches.

Un job d'import utilise **un seul instantané** : téléchargement avec timeout → contrôle du format/en-tête/encodage → normalisation → contrôle des IDs et volumes → aperçu des créations/modifications/retraits → application transactionnelle → publication de bilan et invalidations. Un seuil de retrait inhabituel met le lot en attente, au lieu d'appliquer une désactivation massive. Conserver le dernier lot accepté pour le diagnostic et le rejeu autorisé.

Sources du besoin : `app/entrypoint.sh`, `app/cron/`, `app/Dockerfile`, `docker-compose.yml`, `applications/core/management/commands/`, migrations historiques décrites dans la notice.

## 9. Environnements

| Environnement | Données / services | Usage et protections |
|---|---|---|
| Local | PostgreSQL local, fixtures synthétiques, SMTP capturé, CSV fixture ; HTTPS personnel si nécessaire | Démarrage depuis machine neuve, réseau production inutile, aucune sélection selon OS |
| Test / CI | DB jetable créée par suite de tests, horloge contrôlée, dépendances externes simulées | Isolation entre exécutions, tests de migrations et concurrence, aucun email réel |
| Staging | Même image et schéma cible que production, données synthétiques ou copie anonymisée autorisée, services externes de test | Accès restreint, emails et publication publique neutralisés, jobs activés intentionnellement |
| Production | DB et secrets propres, flux contrôlé, logs/alertes, sauvegardes | Accès limité, changements identifiables, jobs observables |

Fournir `.env.example` sans secret, paramètres explicites d'environnement, commandes de bootstrap documentées, données minimales pour chaque parcours et procédure de remise à zéro **limitée à la DB locale**. Les certificats de développement sont générés personnellement, pas livrés avec leurs clés. L'environnement doit échouer clairement si un paramètre obligatoire manque, et non retomber sur une destination distante.

La première livraison de la refonte devrait rendre possible le parcours topo → saisie → carnet avec plusieurs salles synthétiques, dont une salle mixte, des relais tête et une ouverture retirée. Ce petit jeu donne immédiatement de la valeur aux développeurs sans reproduire une base historique entière.

## 10. Migration des données

### Préparer et mesurer

Obtenir un instantané autorisé de la source et relever schéma effectif, migrations appliquées, volumes, contraintes et contenu réellement utilisé. Sauvegarder source, catalogue et configuration métier, avec un identifiant de lot. Produire un inventaire des données de la section 13 de la notice ; qualifier chaque type en migrer, transformer, recalculer ou abandonner après validation.

Détecter sans les corriger silencieusement : profils absents, doublons de pratique, tops supérieurs aux essais, flash sans réussite, cotations inconnues, références inter-événements, participations multiples, états de paiement et scores initiaux incohérents. Conserver un rapport d'anomalies et les valeurs brutes, sous accès restreint.

### Construire un mapping traçable

Créer une table ou un artefact contrôlé `(type_source, ancien_id, nouvel_id, lot, statut)` et des clés uniques garantissant le rejeu. Un compte et un participant événement sont deux types de source distincts. Ne jamais réutiliser un ID de séance pour signifier une ouverture ; ne jamais fusionner les identités sur un seul nom/email.

Ordre indicatif : salles/emplacements et comptes → profils/rôles/consentements → ouvertures/versions → séances/pratique/projets → compétitions/catalogues/participants/équipes/perfs → dérivés et contenus. Les clés étrangères et relations N:N doivent être vérifiées à chaque étape.

Les scripts futurs vivent dans `scripts/` et la logique de transformation dans `lib/migration/`. Ils ne démarrent pas les services web ni les jobs métier, lisent une source figée et écrivent seulement une cible explicitement choisie. Ils sont versionnés, idempotents, reprenables par lots, avec checkpoints et mode dry-run réellement sans mutation. Ne pas réutiliser les migrations de réparation du POC comme scripts d'import du nouveau produit.

### Transformer sans inventer

Le regroupement historique proposé utilisateur/date/salle/discipline produit des séances reconstituées, marquées comme telles. Garder chaque ligne source rattachée à sa pratique cible. Préserver les compteurs et drapeaux ; une éventuelle conversion en tentatives synthétiques doit être signalée et ne doit pas influencer l'Elo comme une chronologie réelle.

Conserver un instantané des niveaux et scores déjà publiés avant recalcul. Toute correction de formule doit produire une comparaison par utilisateur/discipline/date et par compétition, avec raison et approbation de l'écart. Une nouvelle formule n'efface pas automatiquement l'ancien classement d'un événement clôturé.

### Répéter et comparer

Sur cible jetable : dry-run, migration réelle d'essai, second passage pour vérifier l'idempotence, contrôles d'intégrité et comparaison fonctionnelle. Exiger : chaque ID source important mappé une fois ; sommes essais/tops identiques hors corrections approuvées ; mêmes premières dates de réussite ; mêmes liens de consentement ; mêmes participations/perfs ; compteurs de lignes et références orphelines expliqués.

Comparer aussi des parcours complets : grimpeur multi-salles, voie moulinette puis tête, projet masqué, ouverture inactive, identités atypiques, compétition avec ex æquo et score hérité. Mesurer durée et espace nécessaires pour dimensionner la fenêtre de bascule. Les seules sommes globales peuvent masquer une attribution au mauvais utilisateur : comparer par identité et ouverture.

### Basculer et revenir en arrière

Préférer une première bascule avec **fenêtre de gel des écritures** plutôt qu'une double écriture improvisée. Arrêter anciens jobs et imports, prendre la sauvegarde finale, transférer le delta maîtrisé ou refaire la migration selon durée mesurée, valider les contrôles, basculer le trafic, réémettre les accès nécessaires et invalider les caches/sessions. Planifier hors compétition en cours si possible.

Définir à l'avance critères d'arrêt, responsable de décision, durée maximale et objectif de perte de données accepté. Garder l'ancien système accessible en lecture restreinte pour comparaison.

Rollback avant réouverture des écritures : retour du trafic vers source figée, avec vérification des jobs et caches. **Après nouvelles écritures dans le nouveau MCL, restaurer simplement l'ancienne sauvegarde perdrait ces écritures.** Prévoir soit un transfert inverse testé des nouvelles données, soit une remise en état du nouveau système ; à défaut, maintenir le gel jusqu'à décision. Conserver le journal des mutations après bascule et documenter les opérations manuelles nécessaires. Répéter réellement le scénario retenu en staging.

## 11. Observabilité et maintenance

Un petit ensemble d'outils cohérents suffit : logs structurés centralisés, suivi d'erreurs, table d'exécution des jobs et quelques alertes. Chaque alerte doit avoir un destinataire et une procédure ; aucun de ces messages n'a été envoyé dans le cadre de cette mission.

| Question d'exploitation | Signal à stocker / surveiller | Réaction attendue |
|---|---|---|
| L'import a-t-il échoué ? | ID de lot, source, début/fin, statut, lignes reçues/valides/rejetées, créations/modifications/retraits | Alerte sur échec ou volume anormal, conserver le dernier catalogue accepté, diagnostic et reprise explicite |
| Un cron ne tourne-t-il plus ? | Dernier succès et prochaine échéance, heartbeat du planificateur | Alerte sur absence de succès après échéance + marge, pas seulement sur exception |
| Une API renvoie-t-elle des erreurs ? | Taux d'erreur, latence, route, version, ID de corrélation | Reproduire avec contexte expurgé ; distinguer incident serveur et rejets métier normaux |
| Un niveau est-il incohérent ? | Version moteur, entrées, bornes, variations, différence complet/incrémental sur échantillon | Suspendre publication si nécessaire, recalcul contrôlé, conserver l'ancien résultat consultable |
| Un classement est-il périmé ? | Date sportive, date de calcul, version de règlement, statut de clôture | Afficher la fraîcheur, ne pas servir silencieusement un cache ancien comme résultat du jour |
| Une sauvegarde est-elle utile ? | Dernier backup réussi et dernier exercice de restauration, durée et contrôles | Alerte et exercice périodique ; succès de copie seul insuffisant |
| Un certificat va-t-il expirer ? | Date d'expiration effective servie, résultat du renouvellement | Corriger renouvellement/rechargement avant expiration |

Publier les projections de façon atomique, pour ne pas laisser lire un fichier partiellement réécrit. Mettre un verrou ou une unicité sur les jobs non concurrents. Borner les retries, isoler les lots en échec et éviter qu'un redémarrage provoque une tempête de recalculs.

Les logs ne contiennent pas de secrets, de liens d'accès événement complets ni de données personnelles inutiles. Les identifiants internes suffisent généralement au diagnostic avec accès restreint. Prévoir rotation, rétention définie et espace disque surveillé. Références des limites actuelles : `app/cron/my_cron_jobs`, écritures HTML dans `public_contests/management/commands/generate_daily_ranking.py` et `dir_admin/management/commands/`.

## 12. Documentation minimale à maintenir

| Document | Contenu obligatoire | Quand le mettre à jour |
|---|---|---|
| README | Produit, périmètre, liens utiles, démarrage et tests rapides | Chaque changement d'onboarding |
| Architecture et décisions | Domaines, dépendances autorisées, choix et raisons, schémas simples | Nouvelle frontière ou décision structurante |
| Modèle de données | Entités, relations, contraintes, provenance, suppression et historiques | Chaque évolution de schéma ou migration |
| Règles métier | Règles numérotées, exemples chiffrés, ambiguïtés tranchées, version et validateur | Toute évolution de formule, inscription, progression ou classement |
| Procédure locale | Prérequis, bootstrap, fixtures, HTTPS, SMTP test, remise à zéro locale | Changement de dépendance ou environnement |
| Déploiement | Build, migration, mise en service, jobs, TLS, contrôles et rollback | Changement de chaîne ou infrastructure |
| Restauration | Sauvegardes, accès nécessaires, commande/procédure testée, contrôles, date d'exercice | Après chaque exercice ou évolution de stockage |
| Variables d'environnement | Nom, fonction, obligatoire/défaut, environnement, nature secrète, provenance | Ajout/modification de configuration ; jamais de valeur de production |
| Contrat API | Ressources, erreurs, pagination, idempotence, compatibilité clients | Toute modification de contrat |
| Contrat CSV et jobs | Format, IDs, retrait, validation, horaires, dépendances, diagnostic | Évolution du flux ou d'un traitement |

Ces documents peuvent rester courts et regroupés sous `docs/`. Chaque domaine doit avoir un responsable de mise à jour. Le modèle de PR demande « règle/API/schéma/exploitation impactés ? » et exige les changements correspondants lorsque la réponse est oui. La notice actuelle est un état historique ; les nouvelles règles vivantes ne doivent pas rester enfouies dedans.

## 13. Priorisation

### P0 — indispensable avant toute mise en production

- Sécuriser les accès exposés, supprimer les secrets des nouveaux artefacts et vérifier les droits de l'ancienne production encore utilisée.
- Disposer d'un environnement autonome et d'une cible PostgreSQL isolée ; CI sans accès production.
- Définir et tester permissions par salle, partage de suivi, inscriptions et toutes les écritures publiques.
- Poser le modèle de pratique et les correspondances externes ; préserver l'historique avec migration répétée et écarts approuvés.
- Garantir transactions, contraintes et idempotence sur les écritures critiques ; importer un instantané validé sans retrait massif accidentel.
- Valider les règles et tests de référence du périmètre effectivement livré. Aucun Elo ou règlement de compétition ne doit être publié sans validation de ses calculs.
- Séparer migrations/jobs/web ; disposer d'une sauvegarde restaurée en exercice, d'un rollback réaliste et d'alertes sur erreurs et jobs manquants.
- Définir contrats API et gestion du cache authentifié pour les clients livrés.

P0 ne signifie pas « reconstruire toutes les fonctionnalités avant le premier lancement ». Une fonctionnalité non encore validée peut rester indisponible explicitement ; ses données sont conservées et son remplacement planifié. Une coexistence temporaire avec l'ancien système doit avoir une source d'écriture unique par domaine et des frontières d'accès documentées.

### P1 — important pour la pérennité

- Unifier définitivement les moteurs de progression/classement et versionner états/projections.
- Rendre salles, capacités et catalogues sportifs administrables, avec historique des changements.
- Achever le dictionnaire des indicateurs et corriger la mesure direction ; distinguer connexions, pratique et fréquentation physique.
- Formaliser API/compatibilité, supervision des anomalies de données, runbooks et maintenance régulière des dépendances.
- Automatiser comparaisons de migration et exercices de restauration ; tester concurrence et mises à jour PWA.
- Réduire les dépendances entre domaines et retirer progressivement les adaptateurs de l'ancien produit.

### P2 — amélioration souhaitable

- Ajouter une synchronisation hors ligne complète si le besoin terrain est confirmé.
- Développer une application iOS/Android sur la même API selon les usages natifs attendus.
- Ajouter des analyses avancées, recommandations de projets ou tableaux de bord enrichis sur des métriques fiables.
- Optimiser caches, tâches incrémentales et requêtes à partir de mesures réelles.

Ordre de réalisation proposé : environnement et sauvegarde → décisions métier et mapping → tranche topo/pratique/carnet → projets/statistiques/progression → staff/direction et compétitions selon calendrier → bascule validée. Ne pas attendre la fin du développement pour découvrir les contraintes de migration.

## 14. Critères de réussite de la refonte

- [ ] Sur une machine neuve, un développeur lance l'environnement, les données synthétiques et les tests avec la procédure documentée.
- [ ] Aucune action locale ou CI ne nécessite ni ne sélectionne une DB, un SMTP ou un secret de production.
- [ ] Le dépôt, les artefacts et les images distribués passent le contrôle de secrets ; les accès exposés hérités ont un statut de traitement documenté.
- [ ] Le parcours salle → topo → saisie → carnet fonctionne sur plusieurs salles et disciplines, y compris avec une ouverture retirée.
- [ ] Une double soumission et deux éditions concurrentes ne dupliquent ni n'écrasent silencieusement la pratique.
- [ ] Chaque donnée historique essentielle possède un mapping vérifié ; tout rejet ou transformation est expliqué et approuvé.
- [ ] Les projets, flash, essais/tops et règles tête sont cohérents entre les clients et couverts par les cas métier validés.
- [ ] Les permissions par salle, les URL directes et la révocation d'un partage sont testées sur API, détails et exports.
- [ ] Recalcul complet et incrémental donnent les mêmes résultats à tolérance numérique documentée, y compris après modification/suppression historique.
- [ ] Les règlements livrés produisent les résultats chiffrés attendus, avec dates, précision, population et ex æquo explicites.
- [ ] Les résultats sportifs clôturés restent interprétables après retrait d'une ouverture ou évolution d'une formule.
- [ ] Rejouer un import valide n'ajoute aucun doublon ; un flux vide, invalide ou partiel ne désactive pas le catalogue accepté.
- [ ] L'API possède un contrat exploitable par plusieurs clients ; aucune logique de score ne repose sur l'extraction de HTML.
- [ ] Démarrer ou multiplier les serveurs web ne lance pas les migrations, imports, nettoyages ou recalculs.
- [ ] Une panne d'import, une exécution planifiée manquante et une API en erreur déclenchent un signal exploitable avec une procédure associée.
- [ ] La PWA indique si une saisie est réellement synchronisée et ne montre pas les données d'un ancien compte après déconnexion.
- [ ] La migration finale et le rollback ont été répétés, avec traitement défini des écritures postérieures à la bascule.
- [ ] Une sauvegarde a été restaurée et contrôlée ; les objectifs de temps de reprise et de perte de données sont convenus.
- [ ] Les définitions d'indicateurs ne promettent pas une fréquentation physique ou un historique de connexions que les données ne permettent pas d'établir.
- [ ] Une autre personne que le développeur historique sait déployer, diagnostiquer un job et restaurer l'application en suivant la documentation.

> Référence du dépôt historique, conservée pour l’étude. Les anciens lancements, secrets, certificats et migrations cités ne font pas partie du livrable. Utiliser uniquement `docker-compose.local.yml`, `config.settings_local` et https://localhost:8443.

# My Climbing List — Notice de reprise

Document établi le 10 septembre 2026 par une seconde lecture statique du dépôt. Le rapport `MCL_ANALYSE_TECHNIQUE.md` a été relu puis confronté aux modèles, migrations, vues, calculs, JavaScript, imports et fichiers d'exploitation. Aucune application, migration, connexion DB, commande métier ou import n'a été lancé.

**Ce document transmet un produit et sa connaissance métier ; il ne prescrit pas la conservation du POC.** Le contexte produit vient de la passation ; les comportements décrits viennent du code. Un comportement observé n'est une règle à préserver qu'après validation métier. Les défauts ci-dessous sont déduits statiquement, sans mesure de leur occurrence en production.

Conventions : `applications/` signifie `app/src/applications/` ; tous les autres chemins partent de la racine. Les chemins avec accolades désignent plusieurs fichiers. La copie ne contient pas de répertoire `.git` exploitable : version déployée, historique Git, volumétrie, exploitation effective et sauvegardes restent à vérifier. Les secrets ne sont pas reproduits. Le document complémentaire est [Recommandations pour la refonte](MCL_RECOMMANDATIONS_REFONTE.md).

## 1. À quoi sert My Climbing List ?

Une salle renouvelle régulièrement ses voies et ses blocs. Pour un grimpeur, se souvenir de ce qu'il a essayé, réussi ou laissé en projet devient difficile. MCL relie le catalogue de la salle à un carnet personnel : reconnaître une ouverture, noter sa pratique et comprendre sa progression dans le temps.

Le parcours principal est : **salle → topo → ouverture → saisie de la pratique → carnet → projets → statistiques → progression**. Une réussite en moulinette et une réussite en tête ne représentent pas toujours le même objectif. La répétition d'une voie n'a pas non plus la même signification que la découverte d'une nouvelle voie réussie.

Pour les salles Altissimo, MCL rend le topo consultable et anime la pratique par les contests, événements et classements. Le staff peut observer les ouvertures, accompagner des grimpeurs et organiser des compétitions. La direction dispose d'indicateurs d'usage et de rétention. Ces indicateurs décrivent l'activité **enregistrée dans MCL**, et ne constituent pas une mesure exhaustive des entrées physiques en salle.

Dans l'écosystème Altissimo, le catalogue arrive par un flux CSV topo associé à AltiGest dans les commentaires des dépendances. Le dépôt ne montre pas de synchronisation complète des abonnements, passages au portique ou paiements. Un état « paiement validé » est notamment renseigné par le staff pour les événements ; il ne prouve pas un encaissement intégré. Références : `applications/core/management/commands/update_ouvertures.py`, `app/src/requirements.txt`, `applications/event/models/event_team.py`, `applications/route_event/models/route_event_participant.py`.

## 2. Les utilisateurs et leurs parcours

| Utilisateur | Parcours et bénéfice | Repères |
|---|---|---|
| Grimpeur connecté | Choisir sa salle et sa discipline, consulter topo/plan, sélectionner des ouvertures, saisir date, essais, tops et flash, consulter historique et projets, suivre les graphiques | `applications/core/views/`, `applications/core/static/core/js/` |
| Grimpeur suivi | Autoriser des salles à consulter sa pratique ; retrouver le suivi dans l'espace entraînement | `applications/custom_auth/models/profile.py`, `applications/core/views/training.py` |
| Staff | Se connecter à l'espace staff, gérer contests/inscriptions/équipes, consulter statistiques d'ouvertures, activité et entraînement | `applications/staff_admin/views/` |
| Direction | Consulter des indicateurs transversaux et participants avec le rôle technique superutilisateur actuel | `applications/dir_admin/views/`, `applications/dir_admin/middleware/dir_access.py` |
| Participant à un Contest | Utiliser son compte, s'inscrire, attendre acceptation si payant, saisir des résultats ponctuels ou alimenter un permanent avec le carnet | `applications/contest/views/`, `applications/contest/models/inscription.py` |
| Participant Event / RouteEvent | S'inscrire avec une identité propre à l'événement, choisir un créneau, obtenir un lien personnel, attendre validation du paiement, saisir pendant le créneau | `applications/event/views/team_access.py`, `applications/route_event/views/participant_access.py` |
| Organisateur | Choisir les ouvertures et le règlement, gérer créneaux et participants, valider le paiement, consulter/publier les résultats | `applications/event/views/staff.py`, `applications/route_event/views/staff.py` |

Exemple : un grimpeur essaie une voie trois fois et la réussit une fois en moulinette. Il saisit **3 essais et 1 top**, pas 2 essais et 1 top. La voie apparaît comme réussie au topo et au carnet. Si son relais permet la tête, elle peut rester en projet jusqu'à une réussite en tête. Ce n'est pas contradictoire : les écrans répondent à des questions différentes, mais doivent l'expliquer.

La favorite est un choix utilisateur ; les salles voie/bloc peuvent être calculées à partir de la pratique ; les salles autorisées représentent un partage de données. Ces notions ne doivent pas être confondues avec une affectation professionnelle du staff.

Autre limitation du POC : le décorateur `applications/core/decorators/non_staff_required.py` déconnecte les comptes staff/superutilisateur lorsqu’ils ouvrent les parcours grimpeur concernés. Une même personne ne peut donc pas toujours cumuler naturellement pratique personnelle et rôle professionnel avec ce compte. Ce cloisonnement d’interface n’est pas une règle métier à reconduire sans validation.

## 3. Vocabulaire métier

| Terme | Sens produit et particularité actuelle |
|---|---|
| Salle | Site d'escalade identifié dans le catalogue externe, avec ses particularités de pratique |
| Ouverture | Tracé installé par un ouvreur, avec prises, difficulté, emplacement et date ; peut être une voie ou un bloc. Ne désigne pas l'heure d'ouverture de la salle |
| Ouvreur | Personne qui conçoit et installe les tracés ; champ texte actuel |
| Voie | Parcours grimpé avec une corde, en moulinette ou en tête |
| Bloc | Parcours court sans corde ; utilise les compteurs génériques `nb_try` et `nb_top`, même si certains libellés les appellent moulinette |
| Relais | En escalade, point d'assurage en haut ; dans MCL, numéro d'emplacement d'une voie, utilisé pour décider si la tête est possible |
| Secteur | Zone de blocs ; stockée dans le même entier `relais`, sans entité dédiée |
| Topo | Catalogue ou plan des ouvertures actuellement installées |
| Cotation | Difficulté du tracé, par exemple 6a ou 6a+ ; distincte de la couleur des prises |
| Couleur de cotation | Repère visuel dérivé du niveau ; distinct du champ de couleur de prises |
| Profil / style d'ouverture | Géométrie du mur (dalle, dévers...) / caractère des mouvements (rési, conti, technique...) ; distinct du profil utilisateur |
| Séance | Métier : visite ou période de pratique. Django `Seance` : ligne utilisateur × ouverture × date, avec compteurs agrégés |
| Tentative / essai / try | Une montée ou un essai, réussi ou non ; les tops sont compris dans les essais |
| Échec | Tentative non réussie ; calculé par essais moins tops, et non stocké séparément dans le modèle final |
| Top | Réussite du parcours ; à distinguer de la prise maximale atteinte en compétition voie |
| Flash | Réussite au premier essai ; la portée entre moulinette et tête, les anciennes tentatives et les corrections doivent être validées |
| Moulinette | Corde déjà en place en haut ; canal générique de pratique hors tête dans les compteurs actuels |
| Tête / lead | Le grimpeur clippe la corde en progressant ; canal séparé, disponible selon les relais de la salle |
| Projet | Ouverture essayée mais objectif encore non atteint ; liste dérivée de la pratique, avec possibilité de masquage |
| Niveau du grimpeur | Estimation par discipline, calculée par un Elo adapté ; ce n'est ni une certification ni la plus haute cotation réussie |
| Contest | Compétition liée aux comptes MCL ; permanente ou ponctuelle, classique ou 1000 points, individuelle ou par équipes |
| Permanent | Contest alimenté par le carnet et les ouvertures actives ; son classement peut évoluer avec le renouvellement du topo |
| Event | Famille de compétitions bloc en duos avec identités propres, créneaux et points par bloc |
| RouteEvent | Famille de compétitions voie individuelles, résultat en numéro de prise et « + », classement par moyenne géométrique de rangs |
| Phase | Dans les événements actuels, créneau horaire et capacité ; ne pas supposer un tour sportif autonome avec son propre catalogue |
| Zone | Objectif intermédiaire sur un bloc ; départage ou indicateur selon le règlement |
| Dégaine | Point de clippage intermédiaire d'une voie ; compteur de résultat dans Contest, différent des prises de RouteEvent |
| Alti Ligue | Classement public quotidien construit à partir des niveaux Elo et d'un filtre d'activité |
| Score initial | Valeur mémorisée dans une inscription, héritée d'un autre Contest, ajoutée au score individuel courant |
| Désactivation | Retrait du topo courant sans suppression de l'ouverture ni de ses références historiques |

Sources : modèles des applications `core`, `custom_auth`, `contest`, `event`, `route_event` et calculs détaillés aux sections 5 et 7.

## 4. Modèle métier

Le modèle conceptuel doit séparer l'identité, les lieux, le catalogue, la pratique et les règlements. Un grimpeur pratique une ouverture lors d'une séance ; une compétition sélectionne des ouvertures et recueille des performances selon son règlement. Une autorisation de consulter la pratique appartient à une relation explicite entre grimpeur et salle.

```text
Compte ── Profil / préférences
   ├── Autorisation de suivi ── Salle
   ├── Séance métier ── Pratique ── Ouverture ── Emplacement ── Salle
   ├── Projet ────────────────────────┘
   └── Niveau calculé (discipline, date, version)

Salle ── Compétition ── Catalogue sportif ── Ouverture
              ├── Règlement / créneaux
              ├── Inscriptions ── Participants [compte facultatif]
              ├── Équipes ── Participants
              └── Performances ── Classement calculé / résultat figé
```

Le modèle Django actuel matérialise seulement une partie de ces concepts :

```text
User ──1 Profile ── favorite_salle / salle_voie / salle_bloc ── Salle
          └──────── authorized_salles (N:N) ───────────────────┘
User ──N Seance ──1 Ouverture ──1 Salle
User ──N ClimberLevelDaily (user, bloc, date)
User ──N Inscription ──1 Contest ──N:N Ouverture
User ──N ContestResult ── Contest + Ouverture
User ──N:N Team ── Contest ── initial_contest → Contest

Salle ── Event ── EventPhase / EventParticipant / EventRoute → Ouverture
            └── EventTeam → deux participants + phase
EventParticipant ── EventPerformance ── EventRoute

Salle ── RouteEvent ── RouteEventPhase / RouteEventRoute → Ouverture
RouteEvent ── RouteEventParticipant → phase
RouteEventParticipant ── RouteEventPerformance ── RouteEventRoute
```

Limites structurantes :

- Pas de table séance métier ni de tentative ordonnée. Deux visites le même jour, dans la même salle et discipline, sont indiscernables à partir des seuls regroupements actuels.
- `Seance` ne porte pas de contrainte unique utilisateur/ouverture/date malgré l'utilisation de `update_or_create` sur cette combinaison. Pas de contraintes SQL sur les compteurs.
- `Ouverture.id` et `Salle.id` sont des entiers imposés ; identité interne et identité externe sont confondues. Le relais n'est qu'un entier.
- Modifier la cotation, salle, discipline ou liste des relais agit rétroactivement sur des calculs historiques ; aucune version d'ouverture n'est attachée à la pratique.
- Suppressions en cascade de salle/ouverture/compte : de l'historique sportif peut disparaître. `active=False` ne protège pas contre `delete()`.
- Les participants Event/RouteEvent ne sont pas des `User` ; un email identique ne constitue pas une preuve suffisante pour fusionner leurs identités.
- Le suivi de projet est stocké sur les lignes de pratique, pas sur une relation projet. L'Elo est rangé dans l'application staff alors qu'il sert au produit grimpeur et à l'Alti Ligue.

Sources : `applications/core/models/{seance,ouverture}.py`, `applications/custom_auth/models/`, `applications/staff_admin/models/climber_level_daily.py`, modèles de compétition.

## 5. Fonctionnement des principales fonctionnalités

### Topo

**Besoin :** savoir quoi grimper et retrouver une ouverture. **Actuel :** catalogue actif par salle, séparé voie/bloc, tri relais puis niveau ; badges de réussite dès qu'un top existe dans l'un des canaux. Les projets sont rapprochés du catalogue. La salle peut masquer les cotations récentes : seuil à J−7 inclus, sans borne supérieure sur la date. **Données :** Salle, Ouverture, Seance. **Règle :** renouveler le topo sans perdre le carnet. **Technique :** `applications/core/views/guidebook.py`, `applications/core/utils/views/guidebook.py`, `applications/core/static/core/js/guidebook/`. **Refonte :** définir exactement les limites de masquage, l'ordre des cotations et les droits de consultation ; versionner les plans et emplacements.

### Saisie d'une séance

**Besoin :** noter sa pratique rapidement, y compris après coup. **Actuel :** sélection ordonnée d'IDs, salle/date/discipline et état d'édition en session HTTP ; compteurs et flash préparés dans le navigateur puis envoyés au serveur. Enregistrement par utilisateur/ouverture/date, remplaçant les compteurs existants. Une ligne entièrement à zéro est ignorée. **Données :** Seance et Ouverture ; état local du formulaire. **Règle :** essais totaux comprenant les tops, deux canaux pour les voies, un seul pour le bloc. **Technique :** `applications/core/views/confirm_session.py`, `applications/core/utils/views/session.py`, `applications/core/static/core/js/confirm_session/`. **Limites :** validation JS insuffisamment reprise côté serveur, ajout multi-ouvertures sans transaction globale, collisions de date destructrices en édition. **Refonte :** vraie séance, contrôles serveur, atomicité, traitement explicite des conflits et doubles soumissions.

### Carnet

**Besoin :** conserver visites et accomplissements. **Actuel :** accueil/détails regroupent les lignes de pratique ; le carnet des réalisations agrège par ouverture, conserve la première date de top, cumule essais/tops et propose filtres flash/tête. Les ouvertures démontées restent accessibles aux agrégats ; les niveaux ne commençant pas par 3 à 9 sont exclus du carnet agrégé. **Données :** Seance et catalogue, même inactif. **Technique :** `applications/core/views/{home,details,logbook}.py`, `applications/core/utils/views/{home,logbook,session}.py`. **Limite :** le filtre combiné « flash et tête » signifie « un flash existe et un top tête existe », éventuellement sur deux réalisations différentes. **Refonte :** distinguer journal des séances et palmarès d'ouvertures ; préciser si l'utilisateur cherche une réussite flash en tête.

### Projets

**Besoin :** retrouver ce qu'il reste à réussir. **Actuel :** agrégation historique sur cotations commençant par 3 à 9, ouverture active, au moins un essai, dernière ligne visible. Si relais tête : projet jusqu'au premier top tête ; sinon jusqu'au top générique. Masquer met toutes les lignes existantes à `is_project_visible=False` ; une nouvelle ligne datée plus tard peut le faire réapparaître par sa valeur par défaut. **Technique :** `applications/core/utils/views/projects.py`, `applications/core/refresh_views/projects.py`. **Anomalie :** contrairement à la saisie, le calcul « possible en tête » n'exclut pas explicitement les blocs. **Refonte :** statut et objectif propres au projet, règle commune de discipline, durée du masquage décidée métier.

### Statistiques

**Besoin :** comprendre volume, diversité et types de pratique. **Actuel :** graphiques Plotly d'ascensions, profils/styles et progression ; filtres discipline/date/salle selon écran. Le graphe d'ascensions compte les ouvertures distinctes réussies, privilégie la tête si les deux canaux sont réussis, regroupe les « + » avec la cotation de base et exclut les niveaux inférieurs à 5. Un filtre flash sélectionne des lignes avant agrégation et ne compte pas nécessairement des ascensions individuelles flash. **Données :** Seance + propriétés courantes d'Ouverture. **Technique :** `applications/core/views/graph.py`, `applications/core/utils/graph/`. **Refonte :** dictionnaire d'indicateurs précisant unité, population, période et exclusions ; séparer le calcul des objets Plotly.

### Progression / niveau

**Besoin :** rendre visible l'évolution et motiver. **Actuel :** Elo adapté séparé bloc/voie, conversion cotation et tendances ; calcul à la volée dans le graphe et tables quotidiennes utilisées ailleurs. **Données :** compteurs, flash, cotation actuelle et ordre `created_at`, puis ClimberLevelDaily. **Technique :** `applications/core/utils/graph/progression.py`, `applications/staff_admin/utils/elo_engine.py`, `applications/staff_admin/management/commands/{compute_climber_levels,rebuild_climber_levels,compute_elo_trends}.py`. **Limites :** moteur dupliqué ; reprise incrémentale incomplète ; corrections/suppressions historiques mal détectées. **Refonte :** moteur unique et versionné, état complet, recalcul reproductible, explication accessible à l'utilisateur. Les coefficients sont décrits en section 7, pas validés comme mesure sportive universelle.

### Gestion des salles

**Besoin :** représenter les lieux, les contraintes locales et les préférences. **Actuel :** catalogue de 13 salles codé dans `populate_salles`, plages/listes de relais tête, option de masquage. Le job d'affectation classe les salles par nombre de lignes de pratique sur ouvertures actives divisé par nombre d'ouvertures actives, séparément voie/bloc. Il ne mesure ni le nombre réel d'essais ni le nombre de visites. La favorite reste distincte. **Technique :** `applications/custom_auth/management/commands/{populate_salles,assign_user_salle}.py`, `applications/staff_admin/views/settings.py`, `applications/core/views/settings.py`. **Limites :** `populate_salles` réécrit nom et relais à chaque exécution ; une salle calculée peut rester obsolète si aucun nouveau candidat n'existe. **Refonte :** référentiel administrable, identifiants stables, capacités de pratique historisées, aucune permission dérivée d'une préférence.

### Staff

**Besoin :** exploiter le topo, accompagner et organiser. **Actuel :** statistiques des ouvertures/réussites, grimpeurs actifs, suivi d'entraînement, gestion de contests et exports CSV/PDF. La liste de suivi filtre les profils par `authorized_salles`, mais le calendrier accepte un ID utilisateur avec seulement `is_staff`. **Données :** profils, pratique, catalogue, niveaux, contests. **Technique :** `applications/staff_admin/views/`, notamment `training_list.py`, `training_calendar.py`, `opening_climbers.py`, `openings_stats.py` ; `applications/staff_admin/utils/auth.py`. **Refonte :** rôles par salle et autorisation de suivi vérifiés pour chaque objet, même via une URL directe, avec révocation effective.

### Direction

**Besoin :** suivre l'adoption et l'activité du réseau. **Actuel :** dashboards et caches HTML de fréquentation/rétention. L'activité sur fenêtre de 14 jours combine séances, résultats Contest et dernière connexion de comptes ayant une salle connue. La rétention à un an compare dernière connexion et date d'inscription avec un écart d'au moins 365 jours. **Technique :** `applications/dir_admin/management/commands/generate_frequentation_cache.py`, `applications/dir_admin/utils/retention.py`, vues de direction. **Limites :** `last_login` n'est pas un historique des connexions ; l'affectation aux salles utilise la dernière salle connue aujourd'hui même pour les dates anciennes. Landes manque au dictionnaire de ce graphe et l'ID 14 y est nommé Metz, contre Haut Gazon dans le référentiel. **Refonte :** définir des indicateurs d'usage MCL, conserver les événements nécessaires et éviter les conclusions de fréquentation physique.

### Contests

**Besoin :** animer le topo et organiser une compétition liée au compte MCL. **Actuel :** inscription gratuite active sauf refus ; payante active après acceptation. Catalogue lié au contest, formats classique/1000 points, zones/dégaines, classements général/F/M et équipes. Permanent : succès issus de Seance, ouvertures actives et tête requise sur relais concernés ; ponctuel : ContestResult. Héritage possible d'un score intrinsèque précédent. **Technique :** `applications/contest/models/`, `applications/contest/utils/{scoring,score_initialization}.py`, `applications/contest/views/{classement_topo,submit_result,ranking}.py`. **Limites :** endpoint de saisie trop permissif, populations de dénominateurs différentes, score hérité initialisé lors de consultation, résultat équipe permanent non aligné sur la source Seance. **Refonte :** règlements distincts, fonctions pures et publication datée, inscription et catalogue contrôlés sur chaque écriture.

### Événements bloc

**Besoin :** compétition en duo, sans imposer un compte du carnet. **Actuel :** deux participants distincts d'un même événement, un créneau avec capacité, type de duo calculé selon genres, lien d'accès du duo et validation de paiement. Saisie limitée au créneau inclusif du jour de l'événement. Chaque bloc possède points et option zone ; top implique zone si celle-ci existe. Classement des équipes payées par somme des points des tops, puis nombre de tops, puis zones. Les six premières équipes mixtes de la liste reçoivent un indicateur de qualification. **Technique :** `applications/event/models/`, `applications/event/views/team_access.py`, `applications/event/utils.py`, `applications/event/services/ranking.py`. **Limites :** pas de quota extensible aux ex æquo au sixième ; capacité vérifiée applicativement avec risque de concurrence ; phase = filtre d'équipes, pas de performances distinctes par tour. **Refonte :** valider qualification, catégories, capacité et clôture ; protéger les liens ; figer le barème utilisé.

### Événements voie

**Besoin :** comparer des progressions sur plusieurs voies. **Actuel :** participant individuel, créneau et paiement ; résultat numéro de prise et « + ». Zéro avec « + » interdit. Par voie, prise +0,5 si « + » et rang moyen des places occupées en cas d'égalité. Moyenne géométrique des points de rang sur toutes les voies ; plus petite valeur gagnante, arrondie à trois décimales avant classement, puis davantage de voies tentées départage. **Technique :** `applications/route_event/models/`, `applications/route_event/views/participant_access.py`, `applications/route_event/services/{ranking,route_rankings}.py`, `applications/route_event/utils.py`. **Limites :** absence de résultat = zéro ; genre/phase filtrent l'affichage après le calcul sur tous les participants payés ; pas de référentiel de prise maximale dans le modèle. **Refonte :** faire valider population de classement, absence/abandon, précision et définition du top ; ne pas remplacer ce règlement par celui des contests.

### Alti Ligue

**Besoin :** proposer un classement réseau de progression. **Actuel :** HTML quotidien, deux disciplines, Elo de la veille, jusqu'à 100 lignes sélectionnées par Elo décroissant. Activité depuis J−1−30 jours, toutes disciplines, sans borne haute ; salle favorite prioritaire sur salle calculée ; candidats sans salle éliminés après la limite de 100. Nombre de réussites distinctes calculé sur tout l'historique. **Technique :** `applications/public_contests/management/commands/generate_daily_ranking.py`, `applications/public_contests/views/climber_ranking.py`, `app/cron/generate_alti_ligue_ranking.sh`. **Limites :** peut produire moins de 100 lignes malgré des candidats ; activité future peut qualifier ; succès tête/bloc divergent d'autres écrans ; dépendance forte au bon calcul Elo. **Refonte :** valider éligibilité, période exacte, catégories, ex æquo, affiliation et règles de publication des identités.

## 6. Données externes

Le code télécharge le CSV à l'adresse publique `https://topo.example.test/topos.csv`. Le lien à AltiGest est documenté par les commentaires de `requirements.txt` ; l'outil producteur, le responsable du flux, sa garantie d'exhaustivité et son contrat ne sont pas établis par le dépôt. Aucun appel au flux n'a été effectué pour cette notice.

| Index CSV (base 0) | Usage actuel |
|---|---|
| 0 | Identifiant entier repris directement comme clé primaire Ouverture |
| 1 / 2 / 3 | Nom / date `%Y-%m-%d` / identifiant Salle |
| 5 / 6 | Ouvreur / bloc seulement si valeur exactement `oui` |
| 7 / 8 | Couleur des prises, premier mot / cotation |
| 10 | Relais entier ; zéro ignoré à l'import |
| 11 / 12 | Style / profil, normalisés et traduits |
| 4 / 9 et éventuelles suivantes | Non exploités par ce parseur ; signification à obtenir auprès du producteur |

`fetch_csv_data` effectue un GET sans timeout explicite, détecte l'encodage avec chardet, lit un CSV à virgules et saute l'en-tête. `update_ouvertures` charge les salles et ouvertures, ignore les salles inconnues et lignes invalides, traduit notamment couleurs/cotations portugaises et profils/styles anglais, puis fait des écritures en masse. Toute ouverture importée est activée ; toutes ses propriétés sont remplacées par les propriétés courantes du flux.

`deactivate_old_entries` télécharge **à nouveau** le flux et désactive tout ID absent. Il conserve les lignes et relations historiques, mais n'utilise pas le même instantané que l'import. Un `csv.reader` est un objet vrai même sans ligne : un CSV ne contenant que l'en-tête conduit à un ensemble d'IDs vide et à une désactivation globale. Une réponse partielle ou un HTML renvoyé avec statut 200 peuvent aussi avoir des conséquences graves selon leur parsing. Un flux strictement vide peut échouer dès la lecture de l'en-tête. Ces défauts ne sont pas des règles de retrait du topo.

Sources : `applications/core/utils/management/csv.py`, `applications/core/management/commands/{update_ouvertures,deactivate_old_entries}.py`, `applications/core/utils/core/{i18n_mapping,hold_colors,cotation_colors}.py`.

**Correspondances indispensables à migrer :** identité source de salle, identité source d'ouverture, rattachement ouverture/salle, références des séances et des catalogues sportifs, dates et statut actif. Ne jamais apparier seulement par nom, relais ou couleur : un emplacement est réutilisé lors des renouvellements. Séparer à terme `(système source, ID externe)` de l'ID interne ; conserver une table explicite ancien ID → nouvel ID. Archiver l'état de catalogue au moment de migration, les valeurs brutes et leur provenance quand disponibles ; l'historique des anciennes cotations ne peut pas être reconstruit si la source et les sauvegardes ne le conservent pas.

Autres dépendances connues : PostgreSQL externe et SMTP OVH (`config/settings.py`), Let's Encrypt/Certbot (`docker-compose.yml`), ressources frontend dont Plotly (`app/src/templates/js_components/app_script.html`), plans/icônes/traductions livrés. Vérifier les ressources chargées à distance, leur disponibilité et leurs droits d'utilisation avant redistribution. Aucune intégration de paiement ni API mobile complète n'a été identifiée dans les fichiers examinés.

## 7. Règles métier à préserver

Les règles suivantes forment un **registre de validation**. « Garantie cible » exprime ce que la refonte doit garantir ; les constantes et ambiguïtés nécessitent l'accord du responsable métier.

| Règle et objectif | Implémentation actuelle | Ambiguïté / anomalie | Validation et garantie cible |
|---|---|---|---|
| R01 — Distinguer bloc, moulinette et tête pour décrire réellement la pratique | `core/utils/views/session.py` : tête si non-bloc et relais dans la liste salle | Projets et réussites Alti Ligue n'excluent pas explicitement le bloc dans leur test de relais | Valider les capacités par emplacement ; impossible d'enregistrer de la tête sur un bloc ; règles communes partout |
| R02 — Les essais comprennent les tops | JS `confirm_session/tryInputLogic.js` ; Elo calcule échecs = essais − tops | Entiers libres côté modèle ; POST brut accepté sans imposer tops ≤ essais | Entiers non négatifs, tops ≤ essais par canal ; tests serveur et contraintes DB |
| R03 — Flash décrit le premier essai réussi | JS `iconLogic.js`, historique transmis à confirmation, deux drapeaux et `flash_available` | Déclaration contrôlée surtout par client ; historique et modes non modélisés comme tentatives | Décider si moulinette préalable interdit flash tête, comment corriger un passé et si le flash est unique par ouverture ou mode |
| R04 — Une ouverture peut être réussie et encore en projet tête | `core/utils/views/projects.py` compare tops tête si relais éligible | Une collision secteur bloc/relais tête fausse la décision | Conserver l'objectif tête lorsque pertinent et l'expliquer dans l'interface |
| R05 — Masquer un projet respecte le choix du grimpeur | `core/refresh_views/projects.py` masque les lignes existantes ; dernière date décide | Nouveau jour peut réafficher ; égalités de dates non départagées explicitement | Valider masquage durable, réactivation manuelle/automatique ; stocker décision séparément |
| R06 — Conserver les réalisations après démontage | Carnet sans filtre actif ; projets/topo filtrent actif | Suppression physique en cascade détruit l'historique | Archiver catalogue, protéger les références ; valider exceptions de suppression |
| R07 — Différencier cotation connue, découverte et traduction | Regex 3–9 carnet/projets ; 5–9 Elo/statistiques ; tables de couleurs/traductions | Regex admet des chaînes absentes de la table Elo ; tris texte ; seuils différents | Échelle ordonnée explicite avec inconnue ; valider exclusions et traitement du « + » |
| R08 — L'indicateur d'ascensions mesure ici la diversité | `core/utils/graph/ascension.py` : distinct par ouverture, tête prioritaire, « + » regroupés | Ne représente ni volume de montées ni nombre total de tops | Nommer unité ; proposer séparément volume et diversité ; éviter double compte |
| R09 — Amorcer un niveau avec assez de pratique | `staff_admin/utils/elo_engine.py` : 12 lignes ayant un top, moyenne des difficultés | Ce ne sont ni 12 ouvertures distinctes ni 12 tops ; répétitions d'une même ouverture à plusieurs dates comptent | Valider l'échantillon requis par discipline ; documenter phase sans niveau |
| R10 — Pondérer réussite, flash et tête dans l'Elo | K=10 ; difficulté de 1000 pour 5a à 2450 pour 9c+, pas 50 ; p=1/(1+10^((difficulté−Elo)/50)) ; gains K×(1−p), multiplicateurs 1 / 1,5 flash / 1,25 tête / 1,875 flash tête | Ordre : tops génériques, tops tête, puis échecs ; pas l'ordre réel des essais | Valider formule, coefficients, ordre conventionnel et effet des répétitions ; versionner |
| R11 — Limiter les pénalités répétées sur une ouverture | Même moteur : au plus trois échecs pénalisés par ouverture dans l'état parcouru | Reprise quotidienne ne recharge que l'Elo, pas les compteurs d'échecs ; plafond réinitialisé implicitement | Valider portée vie entière/période ; préserver tout l'état ou rejouer les données ; incrémental = complet |
| R12 — Corriger le carnet doit corriger la progression | `compute_climber_levels.py` détecte `updated_at` sur les lignes restantes | Suppression invisible ; changement de date ne signale pas toujours l'ancienne ; changement de cotation non suivi ; retour anticipé si veille calculée | Journal d'invalidation couvrant création, correction, suppression et catalogue ; recalcul depuis premier jour affecté |
| R13 — Respecter inscription et paiement du Contest | `Inscription.is_active` : refus exclu, payant accepté, gratuit pending admis | Saisie résultats ne vérifie ni inscription, ni ouverture du contest, ni dates | Valider fenêtres et modération ; droits vérifiés dans service de soumission |
| R14 — Permanent lié au topo vivant | `contest/utils/scoring.py` : ouvertures actives, utilisateurs distincts, `created_at ≤ end_date` ou maintenant | Aucun début de période ; date technique plutôt que date de pratique ; démontage change le classement | Valider rétroactivité, date faisant foi, et nécessité de figer un résultat clos |
| R15 — Classic / 1000 points individuels | 1 par ouverture réussie ou 1000/nombre de grimpeurs distincts ; somme tronquée en entier, secondaire = dégaines + zones | Ponctuel : dénominateur peut inclure résultats de non-éligibles ; nombres invalides acceptés en amont | Fixer population du dénominateur, précision et départage ; même calcul pour écran/export |
| R16 — Équipes Contest | `compute_team_scores` : classic nombre de membres ayant topé ; 1000 : n membres × 1000/(adversaires ayant topé + 1) | Source ContestResult même quand classement individuel permanent utilise Seance ; héritage non ajouté à l'équipe | Valider combinaisons autorisées, taille, dénominateur et report des scores |
| R17 — Hériter un score sans le réinitialiser | `score_initialization.py` ne remplit que si NULL ; score intrinsèque précédent, sans chaîne d'héritages | `compute_user_score` permanent ne compte que l'utilisateur : en 1000 points chaque réussite vaut alors 1000 ; lecture de classement écrit le score | Valider instant de gel et propagation ; corriger le dénominateur ; aucune écriture sur consultation |
| R18 — Ex æquo Contest / Event | Rangs 1,2,2,4 selon clés de score ; Event points, tops, zones | Troncature des scores peut créer des égalités ; qualification mixte coupe aux six premiers | Valider précision et extension éventuelle du quota aux ex æquo |
| R19 — Event : top implique zone si le bloc a une zone | `event/models/event_performance.py` vérifie aussi le même événement ; points du top additionnés pour les deux membres | Modification ultérieure de points/zone peut changer l'interprétation passée | Figer le règlement et tracer les corrections ; capacité concurrente testée |
| R20 — RouteEvent : prise et « + », rangs moyens, moyenne géométrique | `route_event/services/ranking.py` ; « + » vaut 0,5 ; absents à zéro ; filtre genre/phase après calcul global | Arrondi avant comparaison ; résultat nul de compétition sans voie ; pas de borne de prises | Valider population, départage, précision, absences et top ; refuser configurations non classables |
| R21 — Créneau d'événement et paiement | `event/utils.py`, `route_event/utils.py` : bornes inclusives à la date de l'événement ; accès participant vérifie paiement | Fuseau global Europe/Paris, y compris Lisboa ; pas de créneau passant minuit explicite | Horodatages/fuseau propres à l'événement ; valider correction organisateur hors créneau |
| R22 — Alti Ligue : niveau publié d'un jour et activité récente | `public_contests/management/commands/generate_daily_ranking.py` | Activité toute discipline, sans borne haute ; limite avant exclusion de salle ; réussites tout historique | Valider période/éligibilité/affiliation/ex æquo ; résultat daté et explicable |
| R23 — Particularités des salles | `populate_salles.py`, `guidebook.py`, `assign_user_salle.py` | Référentiels dupliqués, réécriture au démarrage, affectation calculée dépend du topo actif | Référentiel unique historisé ; préférences ≠ droits ; vérifier cas Landes/Haut Gazon/Lisboa |
| R24 — Suivi et indicateurs doivent respecter leur périmètre | Profile.authorized_salles, liste staff et calculs direction | Calendrier direct ignore consentement ; indicateurs de connexions non historiques | Consentement et rôles à chaque lecture ; définir les indicateurs sans prétendre reconstruire des données inexistantes |

## 8. Architecture technique actuelle

Le dépôt fige Django 5.1.6, Gunicorn 23.0.0 et psycopg2-binary 2.9.10 dans `app/src/requirements.txt`, sur une image Python 3.10 slim. La version réelle de PostgreSQL n'est pas connue. Templates Django, JavaScript natif, CSS et Plotly composent le frontend ; des réponses JSON/fragments existent, sans contrat API métier global.

```text
Navigateur / PWA : HTML + JS + stockage local + Cache Storage
                   │ HTTPS             ↑ réponses possibles du cache
                   ▼
              nginx 80/443 ─────── volume staticfiles
                   │ proxy HTTP
                   ▼
       conteneur app : Gunicorn (7 workers, timeout 120 s)
                   │ WSGI
           Django : middlewares → URLs → vues/templates
                   │ ORM / calculs dispersés
                   ▼
             PostgreSQL externe

Dans app : cron → commandes Django → DB + caches HTML locaux
                        ↑ CSV topo Altissimo
Django → SMTP OVH
Certbot → volumes certificats / challenge partagés avec nginx
```

Dépendances de domaines : `custom_auth` possède salles/profils ; `core` possède ouvertures/pratique ; `contest`, `event` et `route_event` référencent ce catalogue. `staff_admin` possède le niveau utilisé aussi par `core` et `public_contests`. `dir_admin` agrège comptes/pratique/ContestResult. Les migrations font également des dépendances croisées ; `custom_migrations` modifie des identités, et une migration staff importe les modèles et services courants. Ce ne sont pas des frontières métier stables. Les imports globaux via `__init__.py` et les commentaires de chemins périmés compliquent la lecture.

La PWA est un web installé, pas une application native. `app/src/static/base/pwa/config/sw/sw.js` gère installation/activation, invalidations par messages, POST en network-first et beaucoup de pages en cache-first ; statiques et plusieurs back-offices sont exclus de cette interception. La déconnexion vide le cache après un fetch réussi. Il n'y a pas de synchronisation complète des écritures hors ligne identifiée. Le `no-store` HTTP ne remplace pas une politique explicite pour Cache Storage. Version PWA générée à partir de l'heure de chargement des settings, pas d'une version de livraison fixe.

Sources : `app/src/config/{settings,urls,wsgi}.py`, `app/src/templates/`, `applications/services/views/service_worker.py`, service worker et `swFetchLogout.js`, `docker-compose.yml`, `app/Dockerfile`, `app/entrypoint.sh`, `nginx/nginx.conf`.

## 9. Développement local

Lancement historique déclaré, depuis **`app/src`**, avec `DEBUG=True` et `PYTHONUNBUFFERED=1` :

```bash
python manage.py runserver_plus 0.0.0.0:8000 \
  --cert-file certs/localhost/server-certs/localhost.pem \
  --key-file certs/localhost/server-certs/localhost-key.pem \
  --nostatic
```

URL de consultation habituelle : `https://localhost:8000/`. `0.0.0.0` est l'adresse d'écoute, pas l'URL à ouvrir. Dans PyCharm : interpréteur virtuel, script `manage.py`, répertoire de travail `app/src`, variables ci-dessus et arguments de la commande.

Prérequis : Python compatible (3.10 reproduit l'image), dépendances de `requirements.txt`, PostgreSQL **isolé**, schéma et données de test préparés, certificats locaux personnels et confiance configurée, SMTP de test si besoin. `Salle.relais_en_tete` utilise ArrayField : SQLite n'est pas un remplacement immédiat. `--nostatic` délègue les statiques aux routes et à la vue `applications/services/views/static_serve_debug.py` lorsque DEBUG est actif ; leur cache peut masquer les modifications.

**Limite critique : `PROD = platform.system() != 'Darwin'`.** macOS sélectionne une DB locale dont plusieurs paramètres sont codés ; Linux/Windows/Docker sélectionnent les variables DB de production et les hôtes du domaine public. `DEBUG=True` ne sélectionne pas une DB locale. Le `.env` livré ne constitue pas une configuration de développement sûre. Examiner et isoler les paramètres avant toute commande Django. Ne pas utiliser Compose comme bac à sable : il n'apporte pas sa propre DB et déclenche des écritures au démarrage.

La préparation d'une base neuve n'a pas été validée : certaines migrations réparent des données identifiées historiquement, modifient des comptes ou appellent le moteur courant. `runserver_plus` ne crée ni les caches quotidiens ni le jeu de données. HTTPS, cookies sécurisés, origine CSRF et certificat devront être adaptés pour des tests mobiles/LAN. Aucun prérequis n'a été installé pour cette rédaction ; l'exécutable `python` n'est d'ailleurs pas disponible dans le shell de lecture utilisé, tandis que `python3` l'est. Ce constat n'est pas un test de l'environnement historique.

Sources : settings, requirements, `applications/services/urls_non_i18n.py`, `applications/core/migrations/0042_[restauration_individuelle_exclue].py`, `applications/staff_admin/migrations/0005_backfill_missing_climber_elo.py`.

## 10. Production et tâches automatiques

La chaîne décrite dans le dépôt, dont la conformité à la production réelle reste inconnue, construit l'image `app`, copie les sources, installe cron et lance `app/entrypoint.sh`. Celui-ci attend une destination PostgreSQL OVH codée séparément des settings, puis exécute dans cet ordre :

1. `migrate` : modification du schéma **et migrations de données historiques**.
2. `collectstatic --noinput` : publication des statiques.
3. `populate_salles` : remplacement des noms/relais définis dans le code.
4. `update_ouvertures`, puis `deactivate_old_entries` : deux lectures CSV et écritures catalogue.
5. `cleanup_permanent_contests` : suppression d'inscriptions par défaut.
6. `generate_frequentation_cache`, `generate_retention_cache` : fichiers de graphiques.
7. `compute_climber_levels` : écritures/suppressions de niveaux dérivés et tendances.
8. `assign_user_salle`, `generate_daily_ranking` : affectations puis HTML Alti Ligue.
9. Démarrage cron, puis Gunicorn.

**Ce n'est pas une simple commande de démarrage web.** L'entrypoint n'utilise pas d'arrêt global sur erreur : il peut poursuivre après une étape échouée. Redémarrer ou multiplier les réplicas relance ces traitements.

| Horaire du cron fourni | Action | Attention |
|---|---|---|
| Chaque heure, minute 0 | Import et désactivation | Deux téléchargements, absence de validation d'instantané complet |
| 02:00 | Nettoyage permanents | Shell passe `--commit`, option absente de la commande actuelle ; le lancement cron échoue sur cet argument, alors que l'entrypoint sans option supprime réellement |
| 03:00 | Niveaux Elo | Le texte d'aide dit 04:00 mais le cron dit 03:00 ; vérifier fuseau du conteneur |
| 04:00 | Affectation salles + Alti Ligue | Le second job peut tourner après échec du premier ; dépend du niveau de la veille |
| 05:00 | Graphiques fréquentation/rétention | Caches périmés possibles sans indication utilisateur |

Sources : `app/cron/my_cron_jobs`, `app/cron/*.sh`. Le fichier de cron est à la fois copié sous `/etc/cron.d` et installé comme crontab utilisateur : son format sans colonne utilisateur convient au second, pas au premier. Ne pas conclure que tout cron fonctionne correctement à partir de la seule présence du fichier.

Le nettoyage retire une inscription sans succès courant et sans ligne de séance récente sur les ouvertures liées (14 jours, référence `created_at`). Une inscription neuve sans pratique peut être supprimée immédiatement ; le commentaire « 0 point » ne tient pas compte d'un éventuel score initial. Il propose `--dry-run`, mais aucune commande, même simulée, n'a été exécutée ici.

nginx termine HTTPS, redirige HTTP, sert les statiques avec cache d'un an et transmet les en-têtes proxy. Certbot tente le renouvellement toutes les 12 heures et nginx est rechargé toutes les 6 heures. Les certificats utilisent des volumes nommés : le répertoire local `certbot/conf` n'est pas le montage explicitement utilisé par Compose. Le premier approvisionnement, le DNS, les sauvegardes des volumes et les alertes d'expiration sont à vérifier. Les caches HTML ne disposent pas de volume persistant dédié dans Compose.

**Opérations dangereuses identifiées, à encadrer hors de cette mission :** démarrage Compose/entrypoint ; `migrate` et retours de migrations ; `clear_ouvertures` ; import/désactivation ; nettoyage ; reconstruction des niveaux ; génération de fausses données d'événements ; suppression de compte/contest/événement. Sauvegarde restaurable, simulation disponible et périmètre doivent être définis avant leur utilisation.

## 11. Dette technique et pièges de l'existant

| Défaut concret | Conséquence et preuve |
|---|---|
| La séance est un regroupement implicite, sans unicité DB | Doublons possibles et remplacement de données ; `core/models/seance.py`, `core/utils/views/session.py` |
| Changement de date destructeur | L'édition supprime les lignes de la date cible avant de recréer ; les anciennes métadonnées/projet peuvent être perdues ; même fichier |
| Remise à zéro ignorée | Une ligne demandée mais entièrement à zéro ne passe pas dans les lignes supprimées si elle reste sélectionnée ; à caractériser en référence, pas à reproduire |
| Catalogue mutable utilisé comme vérité historique | Modifier une cotation ou salle réinterprète le passé ; import et FK Seance |
| Elo incrémental incomplet | Historique d'échecs perdu, suppressions non détectées ; `staff_admin/management/commands/compute_climber_levels.py` ; `min(impacted.values())` échoue aussi si ensemble vide dans le chemin tendances |
| Comparaisons de dates et ordre fragiles | `date.today()`, `timezone.now().date()`, `localdate()` et ordre `created_at` coexistent ; égalités sans second critère stable dans le moteur |
| Deux voies d'accès au score ne donnent pas forcément le même résultat | Score permanent hérité avec dénominateur limité à un utilisateur ; `contest/utils/scoring.py` |
| Lecture qui écrit | `classement_topo.py` initialise `score_initial` ; une consultation n'est pas nécessairement sans effet de bord |
| Règlements dispersés et HTML utilisé comme interface | `contest/views/ranking.py` appelle/récupère du HTML puis BeautifulSoup pour extraire une partie ; calculs et rendu sont couplés |
| Référentiel des salles copié | `dir_admin/management/commands/generate_frequentation_cache.py` diverge de `custom_auth/management/commands/populate_salles.py` |
| Migrations utilisées comme exploitation | `staff_admin/migrations/0003_wipe_climberleveldaily.py` efface les niveaux ; `0005_backfill_missing_climber_elo.py` importe le code courant ; `core/migrations/0042_[restauration_individuelle_exclue].py` restaure des lignes historiques et son inverse les supprime |
| Transformations d'identité irréversibles | `custom_auth/migrations/0017_slugify_usernames.py` indique que les anciens noms ne sont pas conservés ; `custom_migrations/` modifie aussi identités/droits |
| Caches multi-couches et version non stable | Cache HTML, navigateur, service worker et timestamp des settings ; invalidation dispersée, diagnostic difficile |
| Exploitation confondue avec démarrage | Imports, suppressions, migrations et calculs dans entrypoint, sans séparation de rôles |
| Tests métier absents de la copie examinée | Aucun ensemble de tests applicatifs identifié ; un fichier de migration contenant « test » n'est pas une suite de tests |

La recherche de TODO/FIXME/HACK et commentaires historiques n'a pas fourni de registre de dette utilisable. Les commentaires « identique », les anciens chemins et les routines marquées « test » dans l'entrypoint ne prouvent pas la cohérence du comportement. Les défauts majeurs sont dans les traitements ordinaires et les migrations.

## 12. Sécurité

### Problèmes à corriger immédiatement

- **Secrets et matériel privé présents dans la copie** : `.env` applicatif, paramètres codés dans settings/entrypoint, migrations de comptes, fichiers privés sous `certbot/conf` et certificats locaux. Ne pas les publier, copier dans des exemples ou réutiliser pour le développement. Inventorier puis renouveler/révoquer les accès concernés selon leur portée ; supprimer une valeur du fichier ne la révoque pas. La présence dans cette archive est établie, pas l'étendue de diffusion ni la validité des accès.
- **Soumission Contest insuffisamment autorisée** : `applications/contest/views/submit_result.py` exige une connexion mais pas l'inscription valide, l'appartenance de l'ouverture ou la fenêtre sportive. Vérifier ces conditions côté serveur et valider tout le lot avant écriture.
- **Lecture de suivi hors consentement** : `applications/staff_admin/views/training_calendar.py` autorise tout staff authentifié à sélectionner un grimpeur par ID sans revérifier `authorized_salles`, contrairement à la liste.

### Problèmes architecturaux

Les rôles mélangent `is_staff`, `is_superuser`, `salle_voie` et `favorite_salle`. Les middlewares testent des préfixes non localisés alors que le routage utilise des préfixes de langue ; les contrôles propres aux vues restent donc essentiels. Le cloisonnement ne doit pas dépendre du chemin ni du lien affiché. Sources : `applications/{staff_admin,dir_admin}/middleware/`, `applications/event/permissions.py`, `app/src/config/urls.py`.

Les liens Event/RouteEvent sont des moyens d'accès porteurs : posséder le lien permet d'agir dans son périmètre. Ils sont générés aléatoirement, mais sans expiration/révocation dédiée visible dans les modèles. Prévoir journalisation expurgée, rotation et gestion de perte. Le cache de pages authentifiées impose une politique de séparation utilisateur et de purge, y compris si la déconnexion réseau échoue.

### Éléments à vérifier

Version supportée des dépendances et correctifs applicables au moment de reprise ; permissions DB et infrastructure ; exposition des archives/logs/sauvegardes ; limitation des tentatives d'authentification ; protections des exports et écrans publics ; règles de conservation et suppression ; destinataires des emails ; contrôles objet de toutes les vues staff et des routes localisées ; concurrence sur capacités et inscriptions. Il ne s'agit pas d'un audit d'intrusion ni d'une validation réglementaire.

Des protections existent : CSRF, middleware de sécurité, HTTPS, cookies Secure, génération aléatoire des accès événement et validation de cohérence dans plusieurs modèles Event/RouteEvent. Elles ne compensent pas les défauts de permission objet. Sources : settings, modèles d'événement et `applications/services/views/delete_account.py` (suppression du compte avant envoi d'email, avec cascades).

## 13. Données à préserver pendant la migration

**Principe : sauvegarder une source immuable avant transformation, et ne jamais inventer un historique absent.** Le schéma ne suffit pas : il faut ensuite établir sur une copie autorisée les nombres, doublons, anomalies et références réelles. Ce travail sur données n'a pas été effectué ici.

| Données | Traitement recommandé | Contrôles et limites |
|---|---|---|
| Comptes User, dates d'inscription et identités actuelles | Migrer avec mapping d'ID ; conserver les hachages compatibles ou prévoir réinitialisation | Aucun mot de passe en clair ; ne pas renormaliser les noms sans règle de collision ; invalidation des sessions à la bascule |
| Profils, genre, favorite | Migrer en préservant inconnu/neutre ; transformer les références salle | Ne pas réduire les genres au modèle binaire des événements ; ne pas déduire identité depuis un email |
| Salles voie/bloc calculées | Conserver la valeur de référence puis recalculer selon règle validée | Ce sont des dérivés et non des droits staff ; préserver la favorite choisie |
| `authorized_salles` | Migrer en autorisations explicites, avec provenance « ancien système » | Pas de date de consentement à inventer ; nouvelle collecte si périmètre changé ; révocation testée |
| Droits staff/superuser, groupes et permissions Django éventuels | Transformer en rôles nominatifs par salle ; inventaire et validation manuelle | Ne pas convertir automatiquement une favorite en droit ; ne pas réactiver des comptes désactivés |
| Salles, IDs externes, relais et options | Migrer IDs via table de correspondance ; transformer emplacements et capacités | Inclure plans, noms locaux, correspondances historiques disponibles et fuseaux |
| Ouvertures actives et inactives | Migrer toutes les références et propriétés ; séparer ID source/interne | Pas de fusion par nom/couleur ; conserver un instantané initial et les valeurs inconnues |
| Lignes Seance, compteurs, flash et dates | Transformer en séances et pratique agrégée en conservant chaque ID source | Regroupement proposé utilisateur/date/salle/discipline ; ne prétend pas retrouver plusieurs visites ni ordre des essais |
| `created_at`, `updated_at` | Migrer tels que présents, séparément de la date sportive | Valeurs parfois issues de migrations ; provenance et précision explicites ; conserver pour comparer les anciens calculs |
| Visibilité des projets | Transformer en état par utilisateur/ouverture | Arbitrer lignes contradictoires, dates égales et réapparition ; conserver les valeurs sources avant consolidation |
| ClimberLevelDaily, Elo, tendances | Archiver les valeurs publiées puis recalculer dans un modèle versionné | Une valeur ancienne peut être erronée mais a été vue par l'utilisateur ; comparer, expliquer et valider les écarts |
| Contests, catalogues liés, inscriptions/statuts/score initial, équipes et résultats | Migrer avec leurs relations et règlement historique | Ne pas recalculer silencieusement les scores hérités ; distinguer résultat figé et vue dynamique |
| Event / RouteEvent, phases, participants, paiements validés, équipes, performances | Migrer/transformer sans fusion implicite avec User | Préserver points/zones/prises/« + », ordre des voies, liens de phase ; état paiement ≠ transaction financière |
| Liens d'accès et sessions | Réémettre les accès encore nécessaires ; abandonner les sessions après bascule | Pas de copie dans rapports ; continuité des événements en cours à organiser |
| Popups traduits et vues de messages | Migrer les annonces encore utiles ; éventuellement abandonner les lectures après validation | `core/models/message_popup.py` ; éviter de réafficher des annonces obsolètes |
| Traductions, plans, icônes et textes de règlement | Conserver les contenus utiles et leurs droits, adapter le rendu | `app/src/locale/`, templates/static ; dissocier contenu et présentation |
| Caches HTML, statiques compilés, état PWA | Recalculer / régénérer ; abandonner les artefacts après validation | Ne jamais les utiliser comme substitut de la DB ; archiver un classement publié si seule preuve disponible |
| Logs, sauvegardes et anciennes correspondances | Inventorier séparément ; conserver selon utilité et politique validée | Accès restreint, expurgation des secrets ; données disparues à rechercher sans promettre leur récupération |

Les migrations racontent des changements utiles : scission des salles du profil (`custom_auth/migrations/0014...`, puis autorisations `0015...`), normalisation des identités (`0017...`), passage timestamp → created_at/updated_at (`core/migrations/0038...`), score RouteEvent ajouté puis retiré (`route_event/migrations/0002...`, `0003...`), contraintes et états d'événement retirés (`event/migrations/0002...`, `0004...`). Migrer le **schéma et l'état finaux de la source réelle**, pas rejouer ces réparations sur le nouveau modèle.

## 14. Checklist de reprise

- [ ] Identifier la version de code et le schéma réellement en production, les exploitants et les responsables métier de chaque règlement.
- [ ] Sécuriser les accès exposés et corriger les deux contrôles objets prioritaires ; vérifier les autres endpoints analogues.
- [ ] Obtenir une sauvegarde restaurable et une copie de développement autorisée/anonymisée ; documenter ce qui n'est pas récupérable.
- [ ] Construire un environnement local indépendant avec PostgreSQL, données synthétiques, SMTP de test et flux CSV enregistré.
- [ ] Cartographier les tables réellement peuplées, volumes, contraintes, doublons et cascades sans lancer de nettoyage automatique.
- [ ] Faire valider R01–R24 avec exemples chiffrés, notamment flash, projets, Elo et les trois règlements sportifs.
- [ ] Obtenir le contrat CSV : IDs, exhaustivité, encodage, retrait, disponibilité, responsable et gestion des incidents.
- [ ] Inventorier et tester les permissions par salle, les autorisations de suivi et les catégories publiques.
- [ ] Capturer des jeux de référence du carnet, des calculs et des compétitions avant de remplacer les moteurs.
- [ ] Confirmer quelles fonctionnalités sont réellement utilisées et celles pouvant être retirées avec accord métier.
- [ ] Séparer le démarrage du web, les migrations, les imports, les calculs et le planificateur.
- [ ] Répéter migration et comparaison ancien/nouveau sur copie isolée ; enregistrer chaque écart accepté.
- [ ] Préparer bascule, restauration, rollback et traitement des écritures après bascule avant toute ouverture publique.
- [ ] Livrer d'abord le parcours complet salle → topo → pratique → carnet, puis les domaines suivants selon priorité validée.

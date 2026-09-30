> Référence du dépôt historique, conservée pour l’étude. Les anciens lancements, secrets, certificats et migrations cités ne font pas partie du livrable. Utiliser uniquement `docker-compose.local.yml`, `config.settings_local` et https://localhost:8443.

# My Climbing List — Analyse technique et document de passation

## À lire avant la réunion

**My Climbing List est un monolithe Django orienté web mobile, enrichi de mécanismes PWA.** Les pages sont principalement produites par des templates Django ; le navigateur ajoute les interactions, les graphiques et les caches. En déploiement Docker, nginx termine HTTPS, sert les statiques et transmet les requêtes à Gunicorn/Django. PostgreSQL est externe au Compose. Les imports et calculs planifiés tournent dans le même conteneur que le serveur web. Références : `docker-compose.yml`, `nginx/nginx.conf`, `app/entrypoint.sh`, `app/src/config/settings.py`.

**Le périmètre fonctionnel est déjà riche :** topo des salles, carnet de pratique, projets, progression et statistiques ; outils staff et direction ; contests classiques/permanents ; événements de bloc en duos ; événements individuels de voie ; classement Alti Ligue. Le catalogue des ouvertures vient d'un CSV Altissimo. Références : `app/src/config/urls.py`, `app/src/applications/core/management/commands/update_ouvertures.py`, `app/src/applications/{contest,event,route_event}/`.

**La valeur à préserver est la connaissance métier :** historique des grimpeurs, identifiants externes des ouvertures, distinctions bloc/moulinette/tête/flash, règles de projets, calcul de niveau, règlements et départages des compétitions, particularités de salles, traductions et parcours éprouvés. Il faut transformer ces règles en exemples validés, plutôt que recopier aveuglément leur implémentation. Références : `app/src/applications/core/models/`, `app/src/applications/core/utils/views/projects.py`, `app/src/applications/staff_admin/utils/elo_engine.py`, `app/src/applications/{contest/utils/scoring,event/services/ranking,route_event/services/ranking}.py`.

**La dette apparente est élevée :** contrôles de droits dispersés, dépendances entre apps, calculs de classement partiellement dupliqués, état réparti entre serveur et navigateur, HTML utilisé comme interface interne, migrations de dépannage, absence de tests applicatifs identifiés et démarrage qui cumule opérations sur les données et lancement du serveur. Des anomalies concrètes concernent le cron de nettoyage et la cohérence du calcul Elo incrémental. Références : `app/entrypoint.sh`, `app/cron/cleanup_permanent_contests.sh`, `app/src/applications/contest/views/ranking.py`, `app/src/applications/staff_admin/management/commands/compute_climber_levels.py`.

**Les points de sécurité à signaler sont concrets :** secrets et clés privées présents dans la copie ; endpoint de résultats qui ne vérifie pas l'inscription au contest ; calendrier staff accessible sans revérifier le consentement ; cloisonnement par salle incomplet ; Django 5.1 hors support. Les protections HTTPS, cookies sécurisés et CSRF existent néanmoins. Aucune valeur secrète ne figure dans ce document. Références : `app/src/.env`, `app/entrypoint.sh`, `certbot/conf/`, `app/src/certs/localhost/server-certs/localhost-key.pem`, `app/src/applications/contest/views/submit_result.py`, `app/src/applications/staff_admin/views/training_calendar.py`, `app/src/config/settings.py`.

**Recommandation :** un monolithe Django modulaire avec API REST, PostgreSQL, rôles explicites par salle et calculs métier indépendants des vues. Un web responsive puis une application mobile peuvent consommer la même API. Séparer planification et serveur web ; prévoir un environnement autonome, des données synthétiques et des tests de référence. Pour limiter la dépendance au développeur historique, commencer par un parcours complet et quelques exemples métier validés.

**Point local à retenir :** le lancement habituel est `runserver_plus` en HTTPS depuis PyCharm, avec `app/src` comme répertoire de travail et `DEBUG=True`. `--nostatic` laisse une vue Django personnalisée servir les statiques. Le code choisit cependant le mode local d'après macOS, pas d'après DEBUG : Linux, Windows et Docker prennent la branche production. Références : `app/src/config/settings.py`, `app/src/applications/services/urls_non_i18n.py`, `app/src/applications/services/views/static_serve_debug.py`.

**Phrase d'ouverture proposée :** « Le projet est un POC qui a accumulé de vraies règles métier et des usages concrets. La reprise doit préserver cette connaissance et les données, tout en reconstruisant une base plus cohérente et autonome à maintenir. »

## Périmètre, méthode et conventions

Analyse préparée le 9 septembre 2026 à partir de la copie du dépôt fournie, complétée par les indications du développeur historique sur PyCharm. Inspection de la configuration, modèles, URLs, vues, services, commandes, migrations et de templates et scripts représentatifs. Aucun lancement de serveur, aucune connexion à PostgreSQL, aucune migration ni import n'a été exécuté pour produire ce document. Le seul fichier créé est ce document.

- **Vérifié** : observable dans les fichiers examinés ou les métadonnées publiques des certificats.
- **Déclaré par le développeur** : configuration de lancement PyCharm reproduite dans la section locale.
- **Déduit / à vérifier** : conséquence du code non confirmée par une exécution, ou information absente de la copie.
- Aucun répertoire `.git` exploitable n'est présent : on peut constater la présence des fichiers, pas leur historique de versionnement.
- L'état effectivement déployé, la volumétrie, les usages, les sauvegardes et la validité des accès ne sont pas établis.
- Dans la suite, **`applications/` désigne `app/src/applications/`**. Les autres chemins sont relatifs à la racine du dépôt. Les chemins regroupés entre accolades sont une notation abrégée, pas un nom de fichier littéral.

## 1. Résumé exécutif

My Climbing List est un monolithe Django orienté web mobile, avec une couche PWA.
Le serveur produit principalement du HTML et quelques réponses JSON ou fragments HTML.
PostgreSQL assure la persistance et l'ORM Django constitue le principal accès aux données.
Trois conteneurs sont décrits : application, nginx et Certbot ; la base est externe.
Le catalogue des voies/blocs est importé depuis un CSV Altissimo.
Les grimpeurs enregistrent leur pratique et consultent projets, niveau et statistiques.
Staff et direction disposent d'outils de compétition, suivi et indicateurs d'activité.
Trois systèmes de compétition coexistent : `contest`, `event` et `route_event`.
La valeur accumulée réside dans les règles sportives, les particularités des salles et les parcours.
La dette apparente est élevée, avec des défauts précis de permissions, de cohérence et d'exploitation.

Références : `docker-compose.yml`, `app/src/config/settings.py`, `applications/core/models/`, `applications/{contest,event,route_event}/`.

## 2. Architecture générale

```text
Navigateur / web installé
  HTML, CSS, JavaScript, Plotly
  Service worker + Cache Storage + localStorage/sessionStorage
                         │ HTTPS
                         ▼
                    nginx :443
                     ├── /static/ → volume staticfiles
                     └── autres URL → app:8000
                                           │
                                   Gunicorn, 7 workers
                                           │ WSGI
                                           ▼
                                        Django
                            middlewares → URLs → vues
                                           │
                              fonctions métier / ORM
                                           │
                                           ▼
                                 PostgreSQL externe
                                           │
                       HTML / fragments / JSON / CSV / PDF

Dans app : cron → commandes Django → PostgreSQL et caches HTML
                               └──→ CSV Altissimo
Django → SMTP OVH
Certbot → volumes de certificats partagés avec nginx
```

Une requête dynamique arrive à nginx, qui termine HTTPS et transmet l'hôte, le protocole et l'adresse cliente. Gunicorn appelle `config.wsgi:application`. Les middlewares chargent session, langue, utilisateur et protections ; le routeur sélectionne la vue, qui exploite l'ORM et les fonctions métier. Django rend ensuite un template ou une réponse de données. Les routes fonctionnelles sont préfixées par la langue via `i18n_patterns`.

Toutes les consultations ne suivent pas ce chemin : le service worker peut répondre depuis le cache, et les classements/statistiques peuvent provenir de fichiers HTML précalculés. Références : `nginx/nginx.conf`, `app/entrypoint.sh`, `app/src/config/{wsgi,settings,urls}.py`, `app/src/static/base/pwa/config/sw/sw.js`, `applications/public_contests/management/commands/generate_daily_ranking.py`.

| Service | Rôle |
|---|---|
| `app` | Django, Gunicorn, client PostgreSQL, cron et traitements dans un conteneur |
| `nginx` | Ports 80/443, HTTPS, reverse proxy, statiques |
| `certbot` | Renouvellement des certificats toutes les 12 heures |
| PostgreSQL externe | Données persistantes ; aucun service DB dans Compose |
| SMTP OVH | Courriels, dont réinitialisations de mot de passe |
| CSV Altissimo | Source des ouvertures |

Références : `docker-compose.yml`, `app/Dockerfile`, `app/src/config/settings.py`, `applications/core/utils/management/csv.py`.

## 3. Stack technique

| Élément | Version/configuration | Source |
|---|---|---|
| Python | 3.10, image `python:3.10-slim` | `app/Dockerfile` |
| Django | 5.1.6 | `app/src/requirements.txt` |
| Gunicorn | 23.0.0 ; 7 workers ; timeout 120 s | `app/src/requirements.txt`, `app/entrypoint.sh` |
| nginx | Image sans version fixée | `docker-compose.yml` |
| PostgreSQL | Version serveur inconnue | `app/src/config/settings.py` |
| Pilote DB | psycopg2-binary 2.9.10 | `app/src/requirements.txt` |
| Conteneurisation | Docker Compose ; versions de l'outillage inconnues | `docker-compose.yml` |
| Frontend | Templates Django, HTML/CSS, JavaScript natif et modules ES | `app/src/templates/`, `applications/core/static/core/js/` |
| UI | Bootstrap 5.3.3 ; Font Awesome présent | `app/src/static/base/js/bootstrap/bootstrap.js`, `app/src/static/base/icon_fa/` |
| Graphiques | Plotly Python 6.0.0 ; JS chargé 2.34.0 | `app/src/requirements.txt`, `app/src/templates/js_components/app_script.html` |
| HTTP/imports | requests 2.32.3 ; chardet 5.2.0 | `app/src/requirements.txt` |
| Environnement | python-dotenv 1.0.1 | `app/src/requirements.txt` |
| Formulaires | django-widget-tweaks 1.5.0 | `app/src/requirements.txt` |
| PDF | ReportLab 4.1.0 | `app/src/requirements.txt` |
| Parsing HTML | Beautiful Soup 4.14.3 | `app/src/requirements.txt` |
| Slugs | python-slugify 8.0.4 | `app/src/requirements.txt` |
| Outils locaux | django-extensions 3.2.3 ; Werkzeug 3.1.3 ; pyOpenSSL 25.0.0 | `app/src/requirements.txt` |
| Planification | cron système et commandes Django | `app/cron/my_cron_jobs` |
| HTTPS public | Let’s Encrypt/Certbot, image non versionnée | `docker-compose.yml`, `nginx/nginx.conf` |
| Langues | Français, anglais, espagnol, portugais | `app/src/config/settings.py` |

Les dépendances Python directes sont fixées, mais pas toutes leurs dépendances transitives ni les images. Aucun Django REST Framework ou frontend React/Vue n'a été identifié dans l'architecture examinée. `app/src/node_modules/` est présent, sans `app/src/package.json` ni configuration de build correspondante trouvée. Ce dossier ne prouve donc pas l'existence d'un frontend autonome.

## 4. Organisation du projet

Les onze applications suivantes sont installées dans `app/src/config/settings.py`.

| Application | Objectif et importance | Modèles | Vues et dépendances principales |
|---|---|---|---|
| `custom_auth` | Comptes et salles ; socle central | `Profile`, `Salle`, `User` Django associé | Login, inscription, logout ; importe des validateurs de `core` |
| `core` | Carnet ; cœur fonctionnel | `Ouverture`, `Seance`, popups et traductions/lectures | Accueil, topo, séances, carnet, projets, graphes, profil, suivi ; dépend de `custom_auth` et `staff_admin` |
| `contest` | Compétitions classiques/permanentes | `Contest`, `Inscription`, `ContestResult`, `Team` | Inscription, saisie, classement ; dépend de `core`, `custom_auth` et du cache public |
| `staff_admin` | Back-office salle, suivi sportif | `ClimberLevelDaily` | Contests, inscriptions, équipes, exports, ouvertures, fréquentation, grimpeurs, calendriers |
| `dir_admin` | Vue transversale direction | Pas de modèle propre identifié | Dashboard, participants, fréquentation/rétention ; comptes, salles, séances, contests |
| `public_contests` | Publication et Alti Ligue | Pas de modèle propre identifié | Classements publics ; génération quotidienne depuis les niveaux |
| `event` | Bloc en duos | `Event`, `EventPhase`, `EventParticipant`, `EventTeam`, `EventRoute`, `EventPerformance` | Inscription, accès par lien, gestion staff et classement ; salles/ouvertures |
| `route_event` | Voie individuelle | `RouteEvent`, phases, participants, voies, performances | Accès, gestion, classements, exports ; salles/ouvertures |
| `services` | Infrastructure web/PWA et actions transversales | Aucun propre identifié | Manifest, service worker, viewport, suppression de compte, popup vue |
| `reset_password` | Récupération de compte | Aucun propre | Vues Django et emails localisés |
| `catch_all` | URL inconnues | Aucun | Redirection vers l'accueil |

Références : `applications/<nom>/models/`, `applications/<nom>/views/`, `applications/<nom>/urls.py`, `applications/services/urls_{i18n,non_i18n}.py`.

`app/src/custom_migrations/` est une application installée hors de ce répertoire. Elle réalise des opérations historiques sur les comptes et affectations. `services` n'est pas une couche générale de logique métier : les vrais calculs sont distribués entre `utils`, `services`, vues et commandes.

Le découpage en petits fichiers est positif, mais les frontières sont imparfaites : la salle est dans l'authentification et le niveau sportif dans le back-office staff.

## 5. Modèle de données

```text
User Django
  ├── 1 Profile
  │      ├── salle_voie → Salle
  │      ├── salle_bloc → Salle
  │      ├── favorite_salle → Salle
  │      └── authorized_salles ↔ Salle
  ├── N Seance → Ouverture → Salle
  ├── N ClimberLevelDaily
  └── N Inscription → Contest ↔ Ouverture
                            ├── ContestResult → User + Ouverture
                            ├── Team ↔ User
                            └── initial_contest → Contest

Salle → Event → phases, participants, duos
          └── EventRoute → Ouverture
                  ↑
           EventPerformance ← EventParticipant

Salle → RouteEvent → phases, participants
          └── RouteEventRoute → Ouverture
                  ↑
           RouteEventPerformance ← RouteEventParticipant
```

### Utilisateur, grimpeur et rôles

Le grimpeur connecté est le `User` Django standard complété par `Profile`, sans modèle Climber autonome. Les participants aux événements possèdent une identité séparée et ne sont pas liés aux comptes Django. Références : `applications/custom_auth/models/profile.py`, `applications/event/models/event_participant.py`, `applications/route_event/models/route_event_participant.py`.

Staff et direction sont représentés par `is_staff` et `is_superuser`. Aucun modèle explicite d'appartenance professionnelle à une salle avec rôle n'a été identifié. Références : `applications/staff_admin/decorators/staff_required.py`, `applications/dir_admin/decorators/superuser_required.py`.

### Salle, secteur, relais et ouverture

`Salle` a un identifiant entier explicite et un `ArrayField` PostgreSQL listant les relais de tête. Secteur/relais n'est pas une entité autonome : `Ouverture.relais` est un entier interprété selon `bloc`. Une ouverture porte cotation, couleur de prises, dates, nom, ouvreur, profil, style et état actif. Les identifiants sont repris du flux externe. Références : `applications/custom_auth/models/salle.py`, `applications/core/models/ouverture.py`, `applications/core/management/commands/update_ouvertures.py`.

### Séance, ascension et difficulté

Une ligne `Seance` décrit un utilisateur sur une ouverture à une date, avec compteurs de tentatives et tops, en moulinette/bloc et en tête. Une séance complète est reconstruite par regroupement. Il n'y a pas de tentative individuelle ou d'ascension autonome. La cotation est une chaîne et non un référentiel relationnel. Références : `applications/core/models/seance.py`, `applications/core/utils/views/{home,session}.py`, `applications/staff_admin/utils/elo_engine.py`.

### Intégrité et historique

Les résultats de contest et performances d'événements ont des contraintes d'unicité. `Seance` n'a pas de contrainte `(user, ouverture, date_seance)`, malgré l'usage de `update_or_create` sur ces champs. Les relations de pratique vers ouverture et d'ouverture vers salle sont en `CASCADE` : la suppression physique peut effacer l'historique. La désactivation `active=False` doit rester distincte de la suppression. Références : `applications/core/models/{seance,ouverture}.py`, `applications/contest/models/contest_result.py`, `applications/{event,route_event}/models/`.

## 6. Fonctionnalités principales

| Public | Fonctionnalités | Références |
|---|---|---|
| Grimpeur | Inscription, login pseudo/email, récupération de compte | `applications/custom_auth/views/auth/`, `applications/reset_password/` |
| Grimpeur | Salles, favorite, topo liste/carte, propriétés | `applications/core/views/{salle_list,guidebook,gym_properties}.py`, `applications/core/static/core/js/guidebook/` |
| Grimpeur | Saisie/édition de pratique, carnet, détails | `applications/core/views/{confirm_session,logbook,details}.py` |
| Grimpeur | Projets calculés et masquage | `applications/core/utils/views/projects.py`, `applications/core/refresh_views/projects.py` |
| Grimpeur | Progression, réalisations, profils et styles | `applications/core/views/graph.py`, `applications/core/utils/graph/` |
| Grimpeur | Autorisations de consultation des séances | `applications/core/views/training.py` |
| Staff | Contests, inscriptions, équipes, exports, réglages | `applications/staff_admin/urls.py` |
| Staff | Ouvertures, activité, niveaux, calendriers | `applications/staff_admin/views/{openings_stats,active_climbers,training_calendar}.py` |
| Direction | Dashboard transversal et indicateurs | `applications/dir_admin/views/` |
| Compétitions | Permanent/ponctuel, individuel/équipe, classique/1 000 points, zones/dégaines | `applications/contest/models/contest.py`, `applications/contest/utils/scoring.py` |
| Événements | Duos de bloc, voie individuelle, créneaux, validation, liens personnels | `applications/{event,route_event}/` |
| Public | Classements et Alti Ligue | `applications/public_contests/` |
| Automatisation | Imports, désactivation, nettoyage, Elo, caches | `app/cron/` |

Le suivi d'entraînement est principalement le partage et la consultation du carnet, pas un moteur de programmation d'exercices. « Payant » et « paiement validé » sont des états métier ; aucun prestataire de paiement en ligne n'a été identifié. Références : `applications/core/views/training.py`, `applications/event/views/staff.py`, `applications/route_event/views/staff.py`, `applications/contest/models/inscription.py`.

## 7. Logique métier spécifique à l'escalade

Ces règles représentent une spécification à discuter. Certaines divergences peuvent être voulues ; les anomalies ne doivent pas devenir des exigences de la réécriture.

### Niveau Elo adapté

- Calcul séparé voie/bloc ; cotations retenues commençant par 5 à 9.
- Initialisation après 12 lignes de pratique avec top, par moyenne de leurs difficultés. Ce ne sont pas nécessairement 12 voies distinctes ou 12 ascensions.
- `5a = 1000`, progression de 50 par demi-échelon, jusqu'à `9c+ = 2450`.
- Probabilité : `p = 1 / (1 + 10 ** ((difficulté - niveau) / 50))` ; facteur `K = 10`.
- Gain de base `K × (1 - p)` ; multiplicateurs : 1,5 pour le premier top flash, 1,25 en tête, 1,875 pour le premier flash en tête.
- Pénalité `K × (0 - p)` sur les échecs ; limite de trois par ouverture dans l'état de calcul.

Référence : `applications/staff_admin/utils/elo_engine.py` — `initial_elo_state`, `compute_day`, `_process_seance`, `_adjust_moulinette`, `_adjust_lead`, `_adjust_failures`, `get_difficulty_rating`, `elo_expectation`, `elo2cotation`.

Les résultats quotidiens et tendances sont stockés dans `ClimberLevelDaily`. Le graphique les lit et prolonge les dernières valeurs connues pour sa série quotidienne. Références : `applications/staff_admin/management/commands/{compute_climber_levels,compute_elo_trends}.py`, `applications/core/utils/graph/progression.py`.

### Tête, moulinette, tentatives et flash

Les tentatives incluent les tops : les échecs sont leur différence. Le JavaScript ajuste les tentatives pour les rendre au moins égales aux tops ; le flash utilise aussi des champs cachés et le stockage navigateur. La tête dépend des relais configurés pour la salle. Références : `applications/core/static/core/js/confirm_session/{tryInputLogic,iconLogic,displayFlashIconEdit}.js`, `applications/core/utils/views/session.py` — `get_routes_with_details_optimized`, `applications/custom_auth/management/commands/populate_salles.py`.

### Projets

Un projet est calculé depuis l'historique : ouverture active, tentatives existantes, visibilité conservée sur la dernière ligne. Une réussite en moulinette peut laisser une voie de tête en projet ; un top en tête le termine. Hors tête, le top classique suffit. Référence : `applications/core/utils/views/projects.py` — `get_user_projects`.

### Statistiques de réalisations

L'histogramme déduplique les ouvertures, regroupe les cotations avec/sans `+`, et privilégie la tête si une ouverture a été réussie dans les deux modes. Plusieurs répétitions ne deviennent pas plusieurs voies distinctes. Le filtre flash porte sur les lignes avant agrégation : il mérite des exemples de contrôle quand les modes sont mélangés. Référence : `applications/core/utils/graph/ascension.py` — `get_filtered_seances`, `count_ascensions`.

### Import, cotations et salles

Le CSV normalise cotations portugaises, couleurs, profils et styles ; les relais à zéro sont ignorés et des variantes de gros dévers deviennent « toit ». Références : `applications/core/management/commands/update_ouvertures.py` — `parse_csv_row`, `applications/core/utils/core/i18n_mapping.py`.

Une salle peut masquer les cotations des ouvertures récentes, dans une fenêtre de sept jours. Référence : `applications/core/utils/views/guidebook.py` — `get_recently_opened_ouvertures`.

### Contests classiques et permanents

- Permanent : source `Seance`, ouvertures actives ; tête requise sur les relais concernés, sinon réussite classique ou tête selon la fonction de succès.
- Ponctuel : source `ContestResult`.
- Classique : un point par réussite ; 1 000 points : partage par ouverture entre réussisseurs.
- Équipes en 1 000 points : `réussisseurs de l'équipe × 1000 / (réussisseurs adverses + 1)` par ouverture.
- Ex æquo : rangs `1, 2, 2, 4` ; zones et dégaines participent aux scores secondaires dans les vues concernées.
- Score initial héritable d'un contest terminé ; initialisation persistée une fois.
- Payant : inscription acceptée nécessaire ; gratuit : pending reste actif, refused ne l'est pas.
- Refus/suppression d'inscription retire l'utilisateur des équipes via signaux après commit.

Références : `applications/contest/utils/scoring.py` — `get_success_q`, `compute_permanent_success`, `compute_team_scores`, `assign_ranks_with_ties` ; `applications/contest/utils/score_initialization.py`, `applications/contest/models/inscription.py`, `applications/contest/signals.py`, `applications/public_contests/views/contest_detail.py`.

Les permanents sont répartis en intermédiaire (5), confirmé (6), expert (7), mutant (8–9). Leur nettoyage désinscrit sans réussite et sans activité pertinente récente, seuil de 14 jours par défaut fondé sur `created_at`. Références : `applications/contest/management/commands/{generate_permanent_contests,cleanup_permanent_contests}.py`.

### Événements de bloc en duos

Deux participants distincts du même événement, un duo par participant, capacité par créneau, catégorie homme/femme/mixte déduite. Le classement des équipes validées trie points, tops puis zones. Les six premiers duos mixtes sont marqués qualifiés. Un top implique la zone quand elle existe. Références : `applications/event/models/{event_team,event_performance}.py`, `applications/event/services/ranking.py` — `get_event_ranking`.

### Événements de voie

Performance par numéro de prise ; le `+` vaut 0,5 pour comparer. Les ex æquo d'une voie reçoivent la moyenne des places occupées. Le classement global utilise la moyenne géométrique de ces points, arrondie à trois décimales : plus petit score d'abord, puis nombre de voies effectuées décroissant. Les points par voie sont calculés sur tous les participants validés avant filtrage d'affichage genre/créneau. Référence : `applications/route_event/services/ranking.py` — `get_hold_value`, `compute_ranking_points_for_route`, `get_route_event_ranking`.

### Alti Ligue, affectation de salle et indicateurs

Alti Ligue utilise l'Elo de la veille, une fenêtre d'activité de 30 jours et une sélection de 100 grimpeurs par discipline, avant exclusion éventuelle de ceux sans salle affichable. La salle favorite est prioritaire. Référence : `applications/public_contests/management/commands/generate_daily_ranking.py`.

L'affectation automatique voie/bloc compare par salle le nombre de lignes de pratique sur ouvertures actives au nombre d'ouvertures actives. Ce n'est pas simplement la dernière salle visitée. Référence : `applications/custom_auth/management/commands/assign_user_salle.py` — `compute_best_salle`.

La « fréquentation réelle » mesure l'activité dans l'application sur 14 jours glissants : séances, résultats de contests et certaines connexions, pas les entrées physiques. La rétention à un an constate une connexion au moins 365 jours après inscription, pas une pratique continue. Références : `applications/dir_admin/management/commands/generate_frequentation_cache.py`, `applications/dir_admin/utils/retention.py`.

## 8. Enchevêtrement et dette technique

| Observation | Conséquence | Références sous `applications/` sauf indication |
|---|---|---|
| `core` lit les niveaux de `staff_admin`, qui calcule depuis `core` | Dépendance dans les deux sens | `core/utils/graph/progression.py`, `staff_admin/utils/elo_engine.py` |
| Validateurs d'inscription dans `core` | Auth dépend du carnet | `custom_auth/views/auth/register.py` |
| Salle staff = `salle_voie` ou `favorite_salle` selon l'espace | Sémantique et droits ambigus | `staff_admin/utils/auth.py`, `event/permissions.py`, `route_event/permissions.py` |
| Classement mobile extrait de HTML public par Beautiful Soup | Le DOM devient contrat backend | `contest/views/ranking.py` |
| Scores reconstruits dans plusieurs vues/exports | Divergences possibles | `contest/views/classement_topo.py`, `public_contests/views/contest_detail.py`, `staff_admin/views/export_classement_csv.py` |
| Export initialise `score_initial` | Lecture HTTP avec écriture DB | `staff_admin/views/export_classement_csv.py`, `contest/utils/score_initialization.py` |
| Sessions Django, champs HTML, stockages navigateur et caches | Édition/invalidation difficiles à raisonner | `core/views/confirm_session.py`, `core/static/core/js/confirm_session/`, `app/src/static/base/pwa/config/sw/` |
| Listes de salles codées à plusieurs endroits | Écarts déjà visibles entre peuplement et statistiques | `custom_auth/management/commands/populate_salles.py`, `dir_admin/management/commands/generate_frequentation_cache.py` |
| Événements proches dupliqués | Corrections à reporter | `event/`, `route_event/` |

Exemples de volumes hors dépendances tierces : 484 lignes dans `applications/contest/templates/contest/classement_topo/classement_topo.html`, 458 dans le template public `applications/public_contests/templates/public_contests/contest_detail/contest_detail.html`, 328 dans `applications/staff_admin/management/commands/compute_climber_levels.py`, 317 dans `applications/route_event/views/ranking.py`, 300 dans `applications/contest/utils/scoring.py`. La taille accompagne un mélange de responsabilités ; elle n'est pas un défaut à elle seule.

### Anomalies de cohérence à valider

1. **Elo incrémental** : recharge l'Elo précédent mais réinitialise les échecs par ouverture, alors que leur nombre limite les pénalités. Le recalcul complet peut diverger. Les suppressions de séances ne sont pas capturées par une détection fondée sur `updated_at` des lignes restantes. Référence : `applications/staff_admin/management/commands/compute_climber_levels.py`.
2. **Score individuel permanent 1 000 points** : `compute_user_score` appelle le calcul avec uniquement l'utilisateur cible ; le dénominateur ne couvre pas tous les réussisseurs. Référence : `applications/contest/utils/scoring.py`.
3. **Réussite variable selon l'écran** : topo, projets, permanent et Alti Ligue n'ont pas exactement le même branchement tête/bloc/moulinette. Certaines différences sont légitimes, d'autres à clarifier. Références : `applications/core/utils/views/{guidebook,projects}.py`, `applications/contest/utils/scoring.py`, `applications/public_contests/management/commands/generate_daily_ranking.py`.
4. **Indicateurs historiques reconstruits avec des valeurs actuelles** : dernière salle connue et `last_login` actuel sont utilisés pour les courbes passées. Ce ne sont pas des instantanés historiques fidèles. Références : `applications/dir_admin/management/commands/{generate_frequentation_cache,generate_retention_cache}.py`.
5. **Migrations de maintenance mêlées au schéma** : suppressions de niveaux, comptes staff, popups, normalisations et restauration individuelle. Références : `applications/staff_admin/migrations/0003_wipe_climberleveldaily.py`, `applications/custom_auth/migrations/0010_set_superuser.py`, `applications/core/migrations/0042_[restauration_individuelle_exclue].py`.

L'inspection a recensé 104 migrations numérotées dans les apps et `custom_migrations`. Certaines utilisent les modèles/services courants plutôt que les modèles historiques, par exemple `applications/staff_admin/migrations/0005_backfill_missing_climber_elo.py`. La reproductibilité sur base vierge n'a pas été testée.

Des traces historiques subsistent : ancienne vue commentée dans `applications/catch_all/views/catch_all.py`, ancien chemin de contest dans `app/src/static/base/pwa/config/sw/swNetworkFirst.js`, commentaires de chemins incorrects et popups successives en migrations. Cela ne prouve pas qu'une app entière soit abandonnée.

Aucun fichier de tests Python applicatifs n'a été identifié. L'ORM utilise néanmoins des optimisations locales (`select_related`, agrégations, opérations bulk) et certaines transactions : réutiliser ces intentions. Les commandes Elo et statistiques parcourent utilisateurs/jours, avec des requêtes dans les boucles ; leur coût réel dépend d'une volumétrie non mesurée. Références : `applications/core/management/commands/update_ouvertures.py`, `applications/core/utils/views/session.py`, `applications/staff_admin/management/commands/compute_climber_levels.py`, `applications/dir_admin/management/commands/generate_frequentation_cache.py`.

## 9. Risques techniques et sécurité

### Secrets et fichiers sensibles présents

Aucune valeur secrète n'est reproduite. Leur validité actuelle n'a pas été testée.

| Emplacement | Nature observée |
|---|---|
| `app/src/.env` | Clé Django, secret SMTP et configuration DB |
| `app/entrypoint.sh` | Mot de passe PostgreSQL en clair |
| `app/src/config/settings.py` | Mot de passe local codé en dur |
| `applications/custom_auth/migrations/0010_set_superuser.py` | Mot de passe de compte privilégié |
| `app/src/custom_migrations/migrations/0004_create_staff_loisirama_haut_gazon.py` | Mots de passe staff |
| `certbot/conf/archive/myclimbinglist.app/privkey1.pem` | Clé privée TLS |
| `certbot/conf/accounts/…/private_key.json` | Clé privée du compte ACME |
| `app/src/certs/localhost/server-certs/localhost-key.pem` | Clé privée HTTPS de développement |

Prévoir rotation des accès concernés et retrait des secrets des supports distribués. Le Dockerfile copie tout `app/` ; sans `.dockerignore` identifié, le `.env` et les certificats locaux entrent dans l'image. Le `.gitignore` fourni n'exclut que quelques fichiers système/Python. Références : `app/Dockerfile`, `.gitignore`.

Le certificat public archivé examiné a expiré le 3 juillet 2025. Cela ne décrit pas le certificat servi aujourd'hui par la production. Référence : `certbot/conf/archive/myclimbinglist.app/cert1.pem`.

`app/src/node_modules/`, `app/cron/cron.log`, `.idea/` et des données individuelles dans des migrations sont présents. Leur présence dans la livraison est vérifiée, leur suivi Git ne l'est pas.

### Permissions insuffisantes

| Défaut observé | Détail et référence |
|---|---|
| Résultats de contest | Connexion vérifiée, mais ni inscription/statut, ni dates, ni appartenance de l'ouverture au contest : `applications/contest/views/submit_result.py` |
| Consentement au suivi | La liste filtre `authorized_salles`, le calendrier direct par ID ne le revérifie pas : `applications/staff_admin/views/{training_list,training_calendar}.py` |
| Cloisonnement staff | Validation/refus d'inscriptions sur contest chargé par ID seul ; exports également sans périmètre salle/créateur : `applications/staff_admin/views/{inscriptions,export_classement_csv,export_classement_pdf}.py` |
| Favorite utilisée comme droit | Tout connecté, y compris staff, peut changer sa favorite ; les événements utilisent ce champ comme périmètre : `applications/core/refresh_views/favorite.py`, `applications/{event,route_event}/permissions.py` |
| Middleware et i18n | Tests de préfixes `/staff/` et `/direction/`, alors que les routes ont une langue ; décorateurs présents mais middleware général inopérant pour ces chemins : `applications/{staff_admin,dir_admin}/middleware/`, `app/src/config/urls.py` |

Ces constats proviennent de la lecture du code, sans test d'exploitation. D'autres vues possèdent des contrôles plus restrictifs, par exemple `created_by=request.user` dans `applications/staff_admin/views/{edit_contest,delete_contest}.py` : ne pas généraliser l'absence de droits à tout le back-office.

### Validation et intégrité

`applications/core/utils/views/session.py` accepte directement compteurs et booléens du POST. Les invariants tops ≤ essais, compteurs positifs, légitimité du flash et pratique en tête ne sont pas imposés comme dans le navigateur. L'absence d'unicité de `Seance` expose aussi aux doublons concurrents. Les quotas vérifiés par comptage puis écriture méritent un test concurrent : `applications/staff_admin/views/inscriptions.py`, `applications/event/models/event_team.py`.

### Authentification, CSRF et configuration

Les comptes utilisent authentification/hachage Django ; les validateurs de mot de passe sont configurés et appelés à l'inscription. Le reset utilise les vues Django avec délai d'une heure. Références : `applications/custom_auth/views/auth/{login,register}.py`, `applications/reset_password/views/reset_password.py`, `app/src/config/settings.py`.

Les liens événementiels utilisent des jetons aléatoires de 32 octets. Aucun champ d'expiration n'est visible ; la saisie exige cependant paiement validé et créneau ouvert. Références : `applications/event/models/event_team.py`, `applications/route_event/models/route_event_participant.py`, `applications/event/views/team_access.py`, `applications/route_event/views/participant_access.py`.

- DEBUG vaut False par défaut. Le `.env` fourni ne le fixe pas ; PyCharm le met à True d'après le développeur. L'environnement effectif de production est inconnu.
- HTTPS forcé, HSTS, cookies sécurisés et middleware CSRF sont configurés.
- Aucune exemption `csrf_exempt` n'a été trouvée dans la recherche applicative.
- Aucun dispositif CORS ou API interdomaines dédié identifié.
- Aucun mécanisme anti-tentatives répétées visible dans les vues/nginx inspectés ; le message de login distingue aussi un email inconnu.
- Le mode PROD dépend de l'OS et non de DEBUG.
- PostgreSQL n'a pas de paramètre explicite imposant une vérification TLS ; on ne peut pas en déduire que les connexions effectives sont non chiffrées.

Références : `app/src/config/settings.py`, `nginx/nginx.conf`, `applications/custom_auth/views/auth/login.py`.

Les caches PWA contiennent des pages personnalisées, avec nettoyage à la déconnexion ; les caches ne sont pas explicitement indexés par utilisateur dans la stratégie examinée. Vérifier expiration de session/changement de compte et invalidation. Références : `app/src/static/base/pwa/config/sw/{swCacheFirst,swFetchLogout}.js`.

Django 5.1 est hors support depuis le 3 décembre 2025 ; le projet fixe 5.1.6. Aucun audit CVE exhaustif des autres bibliothèques n'a été effectué. Références : `app/src/requirements.txt`, [calendrier officiel Django](https://www.djangoproject.com/download/).

## 10. Déploiement actuel

### Construction et démarrage

Le Dockerfile installe Python, dépendances, locales, client PostgreSQL et cron ; copie `app/` ; installe la crontab puis définit l'entrypoint. Celui-ci :

1. Attend un serveur PostgreSQL OVH fixé dans le script.
2. Applique les migrations et collecte les statiques.
3. Peuple/met à jour les salles.
4. Importe et désactive les ouvertures.
5. Nettoie les contests permanents.
6. Produit les caches statistiques.
7. Calcule les niveaux, affecte les salles et génère Alti Ligue.
8. Démarre cron puis Gunicorn.

Références : `app/Dockerfile`, `app/entrypoint.sh`. **Démarrer le conteneur est une opération de maintenance des données.** L'entrypoint n'a pas `set -e`, donc des étapes peuvent continuer après un échec.

### Planification

| Horaire déclaré | Traitement |
|---|---|
| Toutes les heures | Import/désactivation des ouvertures |
| 02:00 | Nettoyage des permanents |
| 03:00 | Niveaux Elo |
| 04:00 | Affectations de salles et Alti Ligue |
| 05:00 | Fréquentation/rétention |

Référence : `app/cron/my_cron_jobs`. Ces heures sont celles du conteneur ; le fuseau cron n'est pas explicitement aligné sur celui de Django.

Le shell de nettoyage passe `--commit`, option absente de la commande qui écrit par défaut et propose `--dry-run`. Le démarrage sans cette option peut fonctionner alors que le cron échoue. Références : `app/cron/cleanup_permanent_contests.sh`, `applications/contest/management/commands/cleanup_permanent_contests.py`.

### Volumes, certificats et statiques

Compose définit `staticfiles`, `certbot_letsencrypt` et `certbot_www`. Les statiques collectés sont partagés entre Django et nginx ; `ManifestStaticFilesStorage` crée les références hachées. nginx applique un cache d'un an. Certbot renouvelle toutes les 12 heures ; nginx recharge toutes les six heures. Le dossier local `certbot/conf/` n'est pas monté automatiquement dans ces volumes nommés. La procédure d'initialisation du certificat n'est pas décrite. Références : `docker-compose.yml`, `nginx/nginx.conf`, `app/src/config/settings.py`.

Les caches HTML `cache/dir_admin` et `cache/public_contests` sont dans le conteneur, sans volume dédié. Plusieurs réplicas web auraient chacun leurs caches et leurs cron. Aucun healthcheck, sauvegarde DB ou procédure de restauration n'apparaît dans Compose. La génération des permanents existe mais n'est appelée ni dans l'entrypoint ni dans la liste cron examinée. Références : `docker-compose.yml`, `applications/contest/management/commands/generate_permanent_contests.py`.

### Dépendance externe et risques de l'import

`requests.get` ne fixe pas de timeout ; import et désactivation téléchargent séparément le CSV. Un CSV réduit à un en-tête peut produire un ensemble d'identifiants vide puis désactiver toutes les ouvertures. Le contrôle de complétude manque avant l'opération globale. Références : `applications/core/utils/management/csv.py`, `applications/core/management/commands/{update_ouvertures,deactivate_old_entries}.py`.

Les points à transmettre sont donc : source et contrat CSV, double configuration de connexion DB, bootstrap des certificats, ordre des migrations/données, traitements destructifs, sauvegardes, supervision et durée des recalculs. Leur fonctionnement réel reste à confirmer avec l'exploitation.

## Environnement de développement local

### Lancement habituel déclaré par le développeur

Répertoire de travail PyCharm : **`app/src`**. Commande :

```bash
python manage.py runserver_plus 0.0.0.0:8000 \
  --cert-file certs/localhost/server-certs/localhost.pem \
  --key-file certs/localhost/server-certs/localhost-key.pem \
  --nostatic
```

Variables de la configuration PyCharm :

```text
DEBUG=True
PYTHONUNBUFFERED=1
```

La commande et ces variables sont fournies par le développeur, pas déduites d'une configuration Run PyCharm complète versionnée. Les chemins de certificats et les dépendances correspondantes sont présents. Le répertoire de travail importe aussi pour les lectures relatives du manifest, du service worker et des caches. Références : `app/src/manage.py`, `app/src/certs/localhost/`, `applications/services/views/{manifest,service_worker}.py`, `applications/contest/views/ranking.py`.

### Pourquoi runserver_plus, et rôle des dépendances

`runserver_plus` est fourni par **django-extensions 3.2.3**, installé et déclaré dans `INSTALLED_APPS`. Il utilise **Werkzeug 3.1.3** pour le serveur de développement et son débogueur enrichi ; son support TLS permet de charger certificat et clé. **pyOpenSSL 25.0.0** est également requis par cette version de la commande pour le mode SSL. Références : `app/src/requirements.txt`, `app/src/config/settings.py`, [source de runserver_plus 3.2.3](https://raw.githubusercontent.com/django-extensions/django-extensions/3.2.3/django_extensions/management/commands/runserver_plus.py).

La commande standard `runserver` n'offre pas ces options de certificat. Le choix permet ici de tester directement HTTPS, cookies sécurisés et PWA sans nginx local. C'est une interprétation cohérente du lancement fourni et de `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, tous actifs aussi en local dans `app/src/config/settings.py`.

`PYTHONUNBUFFERED=1` rend les sorties Python immédiatement visibles, sans modifier les droits, la DB ou le mode de déploiement. `DEBUG=True` active le comportement debug Django et la route statique personnalisée ; il ne désactive pas HTTPS ni ne force `PROD=False`.

Ce serveur et son débogueur sont réservés au développement. `0.0.0.0` écoute sur toutes les interfaces IPv4, ce n'est pas l'adresse à saisir dans le navigateur. Utiliser `https://localhost:8000/` ; ne pas exposer ce débogueur sur un réseau non maîtrisé. [Documentation officielle runserver_plus](https://django-extensions.readthedocs.io/en/latest/runserver_plus.html).

### HTTPS et certificats locaux

Fichiers présents :

- `app/src/certs/localhost/server-certs/localhost.pem` : certificat serveur.
- `app/src/certs/localhost/server-certs/localhost-key.pem` : clé privée, non reproduite.
- `app/src/certs/localhost/iOS-certs/rootCA.pem` et `app/src/certs/localhost/avd-certs/rootCA.der` : certificats d'autorité présents dans des dossiers destinés aux clients mobiles ; leur installation et chaîne de confiance effective n'ont pas été vérifiées.

La lecture des métadonnées du certificat serveur montre une validité du **8 avril 2026 au 8 juillet 2028** et des noms autorisés **localhost, 127.0.0.1 et ::1**. Il est dans sa période de validité à la date du document ; cela ne prouve pas que le navigateur lui fasse confiance, ni que la clé corresponde, ces vérifications n'ayant pas été exécutées.

Un nouveau développeur devra disposer d'un certificat local approuvé par son navigateur/système, avec une clé personnelle et les noms réellement utilisés. Ne pas considérer la clé privée livrée comme un secret personnel réutilisable. Les adresses IP LAN ne figurent pas dans les noms examinés : écouter sur `0.0.0.0` ne suffit pas pour tester depuis un téléphone sans adapter certificat, confiance et configuration. Les autorités présentes ne prouvent ni une application native existante ni une procédure mobile opérationnelle.

### Pourquoi --nostatic et comment les statiques sont servis

**Vérifié :** `--nostatic` désactive le wrapper automatique `StaticFilesHandler` de `runserver_plus`. Il ne désactive pas les routes statiques écrites dans le projet. [Source versionnée de la commande](https://raw.githubusercontent.com/django-extensions/django-extensions/3.2.3/django_extensions/management/commands/runserver_plus.py).

Avec `DEBUG=True`, `applications/services/urls_non_i18n.py` ajoute `/static/<path>`. La vue `custom_static_serve` de `applications/services/views/static_serve_debug.py` :

1. cherche le fichier via `django.contrib.staticfiles.finders.find` ;
2. le trouve dans `app/src/static/` ou les répertoires `static/` des applications installées ;
3. retourne une `FileResponse`, ou 404 ;
4. impose `Cache-Control: public, max-age=604800, immutable` (sept jours).

Le but probable de `--nostatic` est donc de laisser cette vue appliquer ses en-têtes au lieu de laisser le wrapper intercepter la requête. L'intention historique reste à confirmer, mais le mécanisme est explicite. **Les statiques locaux sont servis par Django, sans nginx et sans dépendre normalement de collectstatic en DEBUG.** Si DEBUG est False avec ce même lancement, la route personnalisée disparaît et le wrapper reste désactivé : les statiques ne sont plus servis par ce mécanisme.

`NoStoreCacheMiddleware`, ajouté uniquement quand `PROD=False`, applique `no-store` aux réponses HTML, pas aux statiques. Les caches navigateur et PWA restent donc une cause possible d'affichage ancien, malgré DEBUG. Référence : `app/src/config/middleware/cache_control.py`.

Le service worker dispose lui-même d'une réponse à cache long et d'une version générée à l'import des settings. Tester les changements PWA peut nécessiter de contrôler le service worker et les caches dans les outils du navigateur. Références : `applications/services/views/service_worker.py`, `app/src/config/settings.py`, `app/src/static/base/pwa/config/sw/`.

### PostgreSQL local : le piège principal

`PROD = platform.system() != 'Darwin'` dans `app/src/config/settings.py` donne :

- **macOS :** PROD=False ; PostgreSQL sur localhost:5432, rôle et mot de passe locaux codés dans settings ; nom de base lu dans `DB_NAME`.
- **Linux, Windows et conteneur Linux :** PROD=True ; nom, rôle, mot de passe, hôte et port viennent des variables DB.

Les valeurs secrètes ne sont pas reproduites. Sous macOS, changer seulement `DB_USER`, `DB_PASSWORD`, `DB_HOST` ou `DB_PORT` dans l'environnement ne remplace pas les valeurs de la branche locale. Sous Linux/Windows, utiliser le `.env` livré pourrait au contraire sélectionner la DB externe. **DEBUG=True ne corrige aucun de ces comportements.**

Le `.env` est chargé par `load_dotenv()`. Les variables explicitement fournies au processus permettent notamment de définir DEBUG dans PyCharm. Une configuration de développement portable et isolée doit être préparée avant un onboarding Linux/Windows ; elle n'existe pas comme profil distinct prêt à l'emploi dans le dépôt. Rien n'a été modifié ici.

SQLite n'est pas un remplacement immédiat : `Salle.relais_en_tete` est un `ArrayField` spécifique à PostgreSQL. Références : `app/src/config/settings.py`, `applications/custom_auth/models/salle.py`.

### Trois modes à distinguer

**Docker et production ne sont pas deux profils indépendants fournis : Compose décrit déjà un déploiement orienté production.** La production réelle peut avoir des compléments extérieurs au dépôt.

| Point | 1. PyCharm local habituel (macOS) | 2. Docker fourni | 3. Production décrite/inférée |
|---|---|---|---|
| Lancement | `runserver_plus`, commande ci-dessus | entrypoint puis Gunicorn | Même chaîne Gunicorn si Compose utilisé ; état réel non vérifié |
| Mode | PROD=False ; DEBUG=True déclaré | Linux → PROD=True ; DEBUG=False par défaut | PROD=True attendu ; DEBUG réel à confirmer |
| Statiques | Vue Django via finders, DEBUG + nostatic | collectstatic puis nginx, volume partagé | nginx et fichiers hachés selon config |
| HTTPS | Directement Werkzeug avec certificat local | nginx avec certificats du volume Certbot ; Gunicorn en HTTP interne | Domaine public et Let's Encrypt selon config |
| DB | localhost:5432 ; identifiants locaux fixés ; nom via DB_NAME | Django via variables DB ; attente OVH distincte codée dans entrypoint | PostgreSQL OVH attendu ; serveur/version/état effectifs inconnus |
| Hôtes/CSRF | Hôtes `*`, origine de confiance localhost configurée | Domaine public fixé | Domaine public fixé dans les fichiers |
| Code | Sources du workspace, rechargement de développement | Sources copiées dans l'image, pas de montage de code | Nouvelle image/recréation selon procédure à confirmer |
| Traitements | Aucun cron/entrypoint lancé par la commande PyCharm | Migrations, imports, calculs et cron automatiques | Même comportement si déploiement conforme |
| Caches | Statique sept jours + PWA ; no-store HTML | Statique un an ; caches HTML internes | Même configuration décrite |

Références : `app/src/config/settings.py`, `app/Dockerfile`, `app/entrypoint.sh`, `docker-compose.yml`, `nginx/nginx.conf`, `applications/services/views/static_serve_debug.py`.

Les origines CSRF configurées n'incluent pas toutes les adresses/ports de tests possibles. Cela ne signifie pas qu'un POST same-origin sur localhost:8000 échoue automatiquement : vérifier l'origine effective si le navigateur utilise un autre nom, un mobile ou un proxy. Ne pas supprimer CSRF pour contourner un problème de configuration.

### Prérequis pour un nouveau développeur

- Python 3.10 pour reproduire l'image de référence, environnement virtuel dédié et dépendances de `app/src/requirements.txt` ; compatibilité de l'installation locale à tester.
- PostgreSQL isolé, rôle/base adaptés à la branche settings réellement sélectionnée ; données synthétiques ou copie anonymisée autorisée.
- Variables et secrets de développement propres, sans réutiliser les accès SMTP/DB de production.
- Certificat/clé HTTPS locaux et confiance installée ; les fichiers ne suffisent pas à installer la confiance.
- Répertoire de travail `app/src`, interpréteur virtuel choisi dans PyCharm, DEBUG et PYTHONUNBUFFERED configurés.
- Procédure de préparation du schéma/données à valider : les migrations ne sont pas un amorçage garanti d'une base neuve.
- Jeux de données nécessaires aux parcours, et caches statistiques éventuellement absents : `runserver_plus` ne lance pas les traitements Docker.
- SMTP de test ou stratégie locale dédiée pour les parcours d'email ; flux CSV contrôlé ou données de référence pour les imports futurs.

Aucun de ces prérequis n'a été installé ni exécuté durant la rédaction. La section finale donne une tentative de démarrage encadrée.

## 11. À conserver dans une réécriture

| Catégorie | Éléments |
|---|---|
| A — presque tels quels après validation | Correspondances cotations/couleurs/traductions ; données salles/relais ; fonctions simples de classement et ex æquo ; traductions/plans/assets ; données historiques et correspondances d'identifiants |
| B — concept à conserver, implémentation à réécrire | Carnet, Elo, projets, trois règlements de compétition, consentements, intégration CSV, indicateurs, parcours PWA |
| C — abandonner/reconstruire | Secrets embarqués ; démarrage avec maintenance métier ; droits par favorite ; parsing HTML comme interface ; invalidation dispersée ; migrations de dépannage comme exploitation ; calculs dupliqués |

Références : `applications/core/utils/core/`, `applications/custom_auth/management/commands/populate_salles.py`, `applications/contest/utils/scoring.py`, `applications/{event,route_event}/services/ranking.py`, `applications/staff_admin/utils/elo_engine.py`, `applications/contest/views/ranking.py`, `app/entrypoint.sh`, `app/src/custom_migrations/`.

La valeur réside dans les décisions, les cas particuliers et les données. Capturer des exemples de résultats attendus avant d'unifier des comportements différents.

## 12. Proposition d'architecture cible

**Proposition : un monolithe Django modulaire avec API REST et PostgreSQL**, avec couche métier indépendante des vues. Pour une équipe de BUT, éviter de multiplier les services à exploiter.

```text
Web responsive / PWA             Future app iOS / Android
          └──────────── API REST ────────────┘
                            │
                     Django modulaire
             comptes/rôles • salles/ouvertures
             pratique • progression • compétitions
                            │
                        PostgreSQL

Planificateur distinct → imports, statistiques et recalculs
```

Domaines proposés : comptes et rôles par salle/consentements ; catalogue et identifiants externes ; pratique avec séances explicites et réalisations ; progression déterministe/versionnée ; compétitions avec stratégies de classement par règlement.

Un frontend séparé est cohérent avec un mobile futur, sans être un chantier simultané obligatoire : conserver temporairement des templates est possible. Le web et le mobile partageraient l'API, les contrats/types si utile, tandis que scores, permissions et validation restent côté serveur. Le partage d'interface dépendra du choix mobile ultérieur.

Prévoir commandes idempotentes, validation des imports avant application, migrations comme étape de déploiement, paramètres local/test/production explicites, DB locale Compose, données synthétiques et tests de calcul/permissions. La reprise des données devra rapprocher identités, ouvertures et historiques. Il s'agit de recommandations, pas de composants déjà présents.

## 13. Questions probables des étudiants

| Question | Réponse proposée |
|---|---|
| Quel périmètre est vraiment utilisé ? | Le code couvre carnet, stats, staff, direction et trois familles de compétition ; l'usage réel doit être confirmé. Réf. `app/src/config/urls.py`. |
| Tout démarre avec Compose ? | Pas comme sandbox autonome : DB externe et opérations de données au démarrage. Réf. `docker-compose.yml`, `app/entrypoint.sh`. |
| Comment le développeur travaille localement ? | PyCharm, `app/src`, runserver_plus HTTPS, DEBUG=True, nostatic et vue Django de statiques ; macOS sélectionne la branche locale. Réf. section environnement local. |
| D'où viennent les voies ? | CSV Altissimo, identifiants repris dans Ouverture ; contrat et disponibilité à documenter. Réf. `applications/core/management/commands/update_ouvertures.py`. |
| Qu'est-ce qu'une séance en base ? | Ligne utilisateur/ouverture/date avec compteurs, regroupée pour l'écran. Réf. `applications/core/models/seance.py`. |
| Quelle source de vérité pour les résultats ? | Seance pour permanent, ContestResult pour ponctuel, modèles propres pour événements. Réf. `applications/contest/utils/scoring.py`, `applications/{event,route_event}/models/`. |
| Pourquoi une voie réussie reste en projet ? | La réussite en moulinette peut laisser un projet en tête. Réf. `applications/core/utils/views/projects.py`. |
| Comment est calculé le niveau ? | Elo adapté, 12 lignes réussies pour l'initialisation, bonus flash/tête et limite de pénalités ; incrémental à contrôler. Réf. `applications/staff_admin/utils/elo_engine.py`. |
| Pourquoi trois systèmes de compétition ? | Usages différents : carnet/contests, duos bloc, voie individuelle ; mécanismes proches mais règlements différents. Réf. `applications/{contest,event,route_event}/`. |
| Faut-il un compte et comment payer ? | Compte pour contests ; identité et lien personnels pour événements. Paiement validé par état staff, pas de prestataire identifié. Réf. `applications/contest/models/inscription.py`, `applications/event/models/event_team.py`. |
| Comment sont gérés les droits salle ? | Drapeaux Django et champs de profil ; à remplacer par rôles explicites et contrôles systématiques. Réf. `applications/staff_admin/utils/auth.py`, `applications/event/permissions.py`. |
| L'API convient-elle au mobile ? | Endpoints JSON/fragments présents, pas d'API métier stable complète. Réf. `applications/core/refresh_views/`, `applications/contest/views/submit_result.py`. |
| Le hors-ligne est-il complet ? | Consultation en cache et état local ; pas de synchronisation complète des saisies identifiée. Réf. `app/src/static/base/pwa/config/sw/`. |
| Peut-on rejouer les migrations ? | Non validé ; données historiques et services courants peuvent être requis. Réf. `applications/core/migrations/0042_[restauration_individuelle_exclue].py`, `applications/staff_admin/migrations/0005_backfill_missing_climber_elo.py`. |
| Qu'attendre du développeur historique ? | Validation du vocabulaire, règles et exemples ; première livraison étudiante : environnement autonome, carte des données et tests métier pour limiter sa sollicitation. Proposition d'organisation. |

## 14. Antisèche pour la réunion

### Architecture en cinq points

1. nginx reçoit HTTPS et sert les statiques.
2. Gunicorn exécute Django, principalement rendu HTML.
3. PostgreSQL est externe au Compose.
4. Le navigateur ajoute interactions, graphiques et PWA.
5. Imports et calculs tournent avec le web dans le même conteneur.

Repères : `docker-compose.yml`, `nginx/nginx.conf`, `app/entrypoint.sh`, `app/src/config/settings.py`.

### Fonctionnalités à citer

Topo/carnet ; projets ; progression/statistiques ; gestion staff ; direction ; contests classiques/permanents ; duos bloc ; voie individuelle ; Alti Ligue. Repère : `app/src/config/urls.py`.

### Cinq éléments à conserver

1. Historique et identifiants externes.
2. Bloc/moulinette/tête/essai/top/flash.
3. Projets et progression.
4. Règlements et départages.
5. Particularités des salles, traductions et parcours.

Repères : `applications/core/models/`, `applications/core/utils/views/projects.py`, `applications/staff_admin/utils/elo_engine.py`, `applications/contest/utils/scoring.py`, `applications/{event,route_event}/services/ranking.py`.

### Cinq problèmes principaux

1. Secrets et clés dans la livraison.
2. Permissions salle et suivi incomplètes.
3. Démarrage avec maintenance DB et cron incohérent.
4. Couplage calculs/HTML/JS/caches.
5. Tests absents et calculs à réconcilier.

Repères : `app/src/.env`, `applications/staff_admin/views/training_calendar.py`, `applications/contest/views/submit_result.py`, `app/entrypoint.sh`, `applications/contest/views/ranking.py`.

### Cinq conseils aux étudiants

1. Base indépendante et données synthétiques.
2. Dix à vingt exemples métier validés avant réécriture.
3. Droits et validation centralisés côté serveur.
4. Un parcours complet avant élargissement.
5. Documenter démarrage, import et restauration pour être autonomes.

### Vocabulaire

- **Ouverture** : voie ou bloc du catalogue.
- **Seance** : ligne de pratique sur une ouverture à une date.
- **Top / try / flash / lead** : réussite / tentative totale / réussite au premier essai / tête.
- **Profile** : complément du compte, salles et autorisations.
- **ClimberLevelDaily** : niveau quotidien précalculé.
- **Contest / Event / RouteEvent** : trois familles de compétition.
- **Alti Ligue** : classement public fondé sur l'Elo.
- **AltiGest / CSV topo** : source externe des ouvertures.
- **runserver_plus / nostatic** : serveur local HTTPS / délégation des statiques aux routes du projet.

Inconnues à assumer : version déployée, volumétrie, usages, sauvegardes, accès d'exploitation, bootstrap des certificats et validation de l'amorçage d'une base neuve.

## Démarrage rapide pour un repreneur

Ce guide décrit une **tentative encadrée**, pas une procédure de démarrage déjà validée. Aucune commande ci-dessous n'a été exécutée pour ce document. Lancer l'application et naviguer pourra ensuite écrire sessions et données : n'utiliser qu'une DB de développement isolée.

### 1. Préparer une copie de travail et les accès de développement

Obtenir une copie nettoyée des secrets, la version de référence et un jeu de données synthétique ou anonymisé autorisé. Ne pas réutiliser le `.env`, les mots de passe de migrations ou les accès de l'entrypoint pour joindre la production. Ne pas lancer `docker compose up` comme première étape : il applique migrations, imports et nettoyages. Références : `app/src/.env`, `app/entrypoint.sh`.

### 2. Installer Python et les dépendances

Python 3.10 reproduit la base Docker. Exemple POSIX, dans une copie dédiée, depuis la racine :

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/src/requirements.txt
```

Ces commandes créeraient un environnement local mais ne préparent pas la DB. Dans PyCharm, choisir cet interpréteur. Sous Windows, adapter l'activation du venv ; le problème de branche PROD demeure. Références : `app/Dockerfile`, `app/src/requirements.txt`.

### 3. Résoudre la configuration PostgreSQL avant toute commande Django

Lire `app/src/config/settings.py` sans publier ses secrets. Installer ou obtenir un PostgreSQL isolé ; SQLite ne convient pas directement à ArrayField.

- Sur macOS, le code impose localhost:5432 et des identifiants locaux ; seul DB_NAME vient de l'environnement pour cette branche. Il faut une base compatible préparée, ou une future configuration locale adaptée.
- Sur Linux/Windows, PROD=True et les variables DB sont utilisées ; les hôtes autorisés restent ceux de production. Une adaptation locale explicite sera nécessaire avant d'en faire un parcours standard.
- DEBUG=True seul ne suffit pas. Vérifier la destination DB effective sans afficher le mot de passe.

Ne créer aucun compte local en recopiant un mot de passe du document : aucune valeur n'y est fournie. La création de paramètres portables est un travail futur, non effectué ici.

### 4. Préparer le schéma et les données avec une procédure validée

**Blocage connu : le dépôt ne fournit pas un amorçage vierge garanti.** Une migration restaure des séances liées à des IDs historiques ; d'autres manipulent des comptes ou recalculent les niveaux avec le code courant. L'entrypoint migre avant de peupler les salles. Références : `applications/core/migrations/0042_[restauration_individuelle_exclue].py`, `applications/staff_admin/migrations/0005_backfill_missing_climber_elo.py`, `app/entrypoint.sh`.

Faire valider une procédure de création du schéma/données sur une base jetable, ou obtenir une base de développement préparée. Ne pas masquer les erreurs avec des migrations fictivement appliquées. Ce document ne fournit volontairement pas de commande migrate/import à lancer aveuglément. Sans schéma compatible, le serveur pourra signaler des erreurs et les parcours ne fonctionneront pas.

### 5. Préparer HTTPS local

Créer ou obtenir un certificat et une clé personnels de développement pour localhost, et installer la confiance correspondante. Vérifier les chemins attendus dans `app/src/certs/localhost/server-certs/`. Les fichiers présents ne prouvent pas la confiance sur une machine neuve. Pour mobile/LAN, prévoir noms/adresses du certificat et configuration adaptée ; le certificat inspecté ne couvre que localhost et les boucles locales.

### 6. Configurer PyCharm et tenter le lancement

Dans la configuration Run : script `app/src/manage.py`, répertoire de travail `app/src`, interpréteur du venv, variables `DEBUG=True` et `PYTHONUNBUFFERED=1`, plus paramètres de développement validés. Arguments :

```text
runserver_plus 0.0.0.0:8000 --cert-file certs/localhost/server-certs/localhost.pem --key-file certs/localhost/server-certs/localhost-key.pem --nostatic
```

Équivalent terminal POSIX, après préparation de la DB isolée et des certificats :

```bash
cd app/src
DEBUG=True PYTHONUNBUFFERED=1 python manage.py runserver_plus 0.0.0.0:8000 \
  --cert-file certs/localhost/server-certs/localhost.pem \
  --key-file certs/localhost/server-certs/localhost-key.pem \
  --nostatic
```

Ouvrir `https://localhost:8000/`. L'adresse d'écoute n'est pas l'URL du navigateur. Le serveur de développement contrôle notamment les migrations, mais cette commande n'applique pas l'entrypoint Docker ni ses imports/cron.

### 7. Contrôler les symptômes sans lancer les traitements de production

| Symptôme | Vérification à effectuer |
|---|---|
| Commande inconnue ou module absent | Interpréteur PyCharm et dépendances du venv |
| Erreur certificat | Chemins relatifs, confiance, validité et noms autorisés |
| DisallowedHost sur Linux/Windows | Branche PROD sélectionnée par l'OS |
| Erreur PostgreSQL | DB isolée, paramètres effectifs et schéma préparé |
| CSS/JS absents | DEBUG=True, URL `/static/`, fichiers source et vue `custom_static_serve` |
| Changement frontend invisible | Cache sept jours, service worker et Cache Storage |
| Erreur CSRF | Origine réellement utilisée, HTTPS et cookies ; ne pas désactiver la protection |
| Classements/graphes indisponibles | Données et caches précalculés non créés par le lancement local |
| Reset/email en erreur | SMTP de test non préparé |

Références : `app/src/config/settings.py`, `applications/services/views/static_serve_debug.py`, `applications/services/views/service_worker.py`, `applications/contest/views/ranking.py`, `applications/dir_admin/views/frequentation.py`.

**Livrable recommandé aux repreneurs :** une procédure reproductible avec PostgreSQL local, configuration d'environnement explicite, secrets personnels, fixtures synthétiques et tests métier. Ce sera la première étape pour rendre le projet indépendant de la machine et de la disponibilité du développeur historique.

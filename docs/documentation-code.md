# Documentation du code – MyClimbingList
 
*Dernière mise à jour : 25/11/2026 – Version : 0.1*
 
Cette documentation est destinée aux développeurs qui reprendront le projet.
Elle reste volontairement légère : le code doit s'expliquer lui-même, et nous documentons uniquement ce qu'il ne dit pas
(architecture, responsabilités des composants, API, choix structurants).
Les instructions du code ne sont pas commentées ligne par ligne.
 
## 1. Vue d'ensemble de l'architecture
 
MCL est composé de deux parties qui communiquent par une API REST en JSON :
 
| Composant | Technologie | Dossier | Responsabilité |
|---|---|---|---|
| Application mobile | Flutter | `frontend/` | Interface utilisateur, appels à l'API |
| API et backoffice | Symfony 7.4, PHP 8.4 | `backend/` | Logique métier, authentification, accès aux données, backoffice d'administration |
| Base de données | MySQL (accès via Doctrine ORM) | – | Stockage des données |
 
```
[ Application Flutter ] --HTTP/JSON (jeton JWT)--> [ API Symfony ] --Doctrine--> [ MySQL ]
                                                        |
                                                  [ Backoffice EasyAdmin ]
```
 
> **À compléter (Front)** : schéma plus détaillé si besoin.
 
## 2. Backend (Symfony)
 
### 2.1 Organisation du code
 
| Dossier | Contenu |
|---|---|
| `backend/src/Entity/` | Entités Doctrine (modèle de données) |
| `backend/src/Enum/` | Énumérations PHP (`TypeOuverture`, `StatutOuverture`) |
| `backend/src/Controller/` | Contrôleurs de l'API |
| `backend/src/Command/` | Commandes console (`app:creer-admin`) |
| `backend/migrations/` | Migrations Doctrine : la base peut être reconstruite à partir d'elles |
| `backend/config/packages/security.yaml` | Pare-feu, contrôle d'accès, hiérarchie des rôles |
| `backend/tests/` | Tests PHPUnit (voir le [cahier de recette](./cahier-de-recette.md)) |
 
### 2.2 Modèle de données (version 1)
 
La migration de la version 1 crée 6 tables.
 
| Entité | Rôle |
|---|---|
| `Salle` | Une salle d'escalade du réseau Altissimo |
| `Utilisateur` | Un compte (grimpeur, staff ou direction) |
| `Ouverture` | Une voie ou un bloc ouvert dans une salle (type et statut portés par des enums PHP) |
| `Seance` | Une séance d'escalade d'un utilisateur |
| `Grimpe` | Une voie grimpée pendant une séance |
| `Suivi` | Autorisation donnée par un utilisateur à une salle de consulter ses séances |

> Le détail se trouve dans [`docs/backend`](./backend).
 
### 2.3 Sécurité
 
- **Authentification de l'API** : jeton JWT (bundle Lexik JWT). Le jeton est envoyé dans l'en-tête `Authorization: Bearer <jeton>`.
- **Renouvellement du jeton** (refresh token avec rotation) : prévu, pas encore implémenté.
- **Protection IDOR** : un utilisateur ne doit accéder qu'à ses propres ressources (séances, carnet) ; à vérifier endpoint par endpoint.
- **Données sensibles** : `GET /api/me` n'expose ni le mot de passe ni les rôles (testé).
- **Backoffice** : accès sous `/admin`, protégé par `access_control` et une hiérarchie de rôles dans `security.yaml`.
  Rôles prévus : `ROLE_STAFF` et `ROLE_DIRECTION`.
  - utilisateur simple : aucun accès ;
  - staff : sa salle, et les séances et grimpes des utilisateurs ayant autorisé sa salle ;
  - direction : accès à tout.
  Le lien entre un membre du staff et sa salle (relation `sallesGerees`) est en place ; le filtrage par salle et les droits fins
  (voter EasyAdmin) sont en pause en attendant la validation du client.
### 2.4 API
 
Format : JSON. Préfixe : `/api`. Documentation de conception : [`docs/backend`](./backend).
 
| Méthode | Route | Description | Accès | État |
|---|---|---|---|---|
| POST | `/api/auth/login` | Connexion, renvoie un jeton | Public | Implémenté |
| GET | `/api/me` | Profil de l'utilisateur connecté | Jeton requis | Implémenté |
| GET | `/api/salles` | Liste des salles | Public | Implémenté |
| POST | `/api/auth/register` | Création de compte | Public | Prévu |
| POST | `/api/auth/refresh` | Renouvellement du jeton | Public | Prévu |
| POST | `/api/auth/password-reset` | Réinitialisation du mot de passe | Public | Prévu |
| PATCH | `/api/me` | Modification du profil | Jeton requis | Prévu |
| GET | `/api/ouvertures` | Liste des ouvertures | À définir | Prévu |
| GET / POST | `/api/seances` | Séances de l'utilisateur | Jeton requis | Prévu |
| GET | `/api/carnet` | Carnet de l'utilisateur | Jeton requis | Prévu |
| GET | `/api/grimpes` | Grimpes, avec filtres côté backend (ex. voies grimpées mais non topées) | Jeton requis | À définir (demande du front) |
 
### 2.5 Tests
 
Voir le [cahier de recette](./cahier-de-recette.md). Lancement : `cd backend && php bin/phpunit`.
 
## 3. Frontend (Flutter)
 
> **À compléter (Front)**
 
### 3.1 Organisation du code
 
| Dossier | Contenu |
|---|---|
| `front/lib/...` | |
| | |
 
### 3.2 Gestion de l'état et navigation
 
> **À compléter (Front)** : solution choisie (Provider, Riverpod, Bloc, etc.) et organisation des écrans.
 
### 3.3 Communication avec l'API
 
> **À compléter (Front)** : client HTTP utilisé, stockage du jeton, gestion de l'expiration du jeton.
 
### 3.4 Composants et écrans principaux
 
| Écran / composant | Rôle | Fichier |
|---|---|---|
| | | |
 
## 4. Conventions de contribution
 
 
### 4.1 Nommage des branches
 
Les branches sont séparées par partie du projet (backend ou frontend), puis par fonctionnalité :
 
| Partie | Format |
|---|---|
| Backend | `backend/feature/<nom-de-la-fonctionnalité>` |
| Frontend | `frontend/feature/<nom-de-la-fonctionnalité>` |
 
### 4.2 Circuit de fusion
 
**Backend** : la branche de fonctionnalité est fusionnée directement dans `main` par pull request.
 
```
backend/feature/<nom>  --PR + review-->  main
```
 
**Frontend** : la branche de fonctionnalité est fusionnée dans `frontend/main`, puis `frontend/main` est fusionnée dans `main` par pull request.
 
```
frontend/feature/<nom>  --merge-->  frontend/main  --PR + review-->  main
```
 
### 4.3 Revue de code
 
- Toute pull request vers `main` nécessite une **review par un membre de l'équipe autre que son auteur**.
- L'auteur ne valide pas sa propre pull request.

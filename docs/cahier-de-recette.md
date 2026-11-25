# Cahier de recette – MyClimbingList

*Dernière mise à jour : 25/11/2026 – Version du cahier : 0.1*

## 1. Objectif et périmètre

Ce cahier décrit les tests réalisés pour vérifier que MyClimbingList (MCL) se comporte comme attendu.

| Composant | Type de tests | État |
|---|---|---|
| Backend (API Symfony) | Tests d'intégration API automatisés (PHPUnit) | Quelques tests en place |
| Base de données | Tests dédiés | Pas encore de tests |
| Frontend (Flutter) | Tests unitaires / widgets / recette manuelle | Pas encore de tests |

## 2. Environnement de test

| Élément | Valeur |
|---|---|
| Framework de test backend | PHPUnit |
| Emplacement des tests backend | `backend/tests/Api/` |
| Base de données | TBD : Base de test dédiée |
| Lancement local backend | `cd backend && php bin/phpunit` |
| Intégration continue | TBD : Pipeline GitHub Actions |

## 3. Description des tests d'intégration (Backend)

Les tests d'intégration appellent l'API comme le ferait l'application mobile : une requête HTTP est envoyée,
puis le code de réponse et le contenu JSON sont vérifiés. Ils traversent donc le routage, la sécurité (jetons) et les contrôleurs.

### 3.1 Authentification et profil

Fichier : `back/tests/Api/AuthEtProfilTest.php`

| ID | Cas de test | Pré-conditions | Étapes | Résultat attendu | Type | Automatisé | Statut |
|---|---|---|---|---|---|---|---|
| CT-API-01 | Connexion avec identifiants valides | Utilisateur `a@test.fr` existant | `POST /api/auth/login` avec l'email et le bon mot de passe | Code 200 et un jeton non vide dans la réponse | Intégration API | Oui | Réussi |
| CT-API-02 | Connexion avec mauvais mot de passe | Utilisateur `a@test.fr` existant | `POST /api/auth/login` avec l'email et un mauvais mot de passe | Code 401 | Intégration API | Oui | Réussi |
| CT-API-03 | Accès au profil sans jeton | Aucune | `GET /api/me` sans jeton | Code 401 | Intégration API | Oui | Réussi |
| CT-API-04 | Accès au profil avec jeton falsifié | Aucune | `GET /api/me` avec un jeton invalide | Code 401 | Intégration API | Oui | Réussi |
| CT-API-05 | Profil sans données sensibles | Utilisateur `a@test.fr` existant et connecté | `GET /api/me` avec un jeton valide | Code 200, email correct, absence des champs `password` et `roles` | Intégration API | Oui | Réussi |

### 3.2 Salles

Fichier : `back/tests/Api/AuthEtProfilTest.php`

| ID | Cas de test | Pré-conditions | Étapes | Résultat attendu | Type | Automatisé | Statut |
|---|---|---|---|---|---|---|---|
| CT-API-06 | Liste des salles accessible sans connexion | Aucune | `GET /api/salles` sans jeton | Code 200 et un tableau JSON | Intégration API | Oui | Réussi |

## 4. Tests de la base de données

Aucun test dédié pour le moment.

| ID | Cas de test | Pré-conditions | Étapes | Résultat attendu | Type | Automatisé | Statut |
|---|---|---|---|---|---|---|---|
| CT-BD-01 | *À définir* | | | | | | |

## 5. Tests du frontend (Flutter)

Aucun test pour le moment.

| ID | Cas de test | Pré-conditions | Étapes | Résultat attendu | Type | Automatisé | Statut |
|---|---|---|---|---|---|---|---|
| CT-FRONT-01 | *À définir* | | | | | | |

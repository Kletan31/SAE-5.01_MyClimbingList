# Documentation utilisateur – MyClimbingList

*Dernière mise à jour : 26/11/2026 – Version : 0.2*

Cette documentation aide les utilisateurs de MCL, l'application des salles d'escalade Altissimo.
Elle ne détaille pas ce que l'interface rend évident (par exemple la saisie d'un email et d'un mot de passe) :
elle se concentre sur ce qui demande une explication.

## 1. À qui s'adresse MCL ?

| Profil | Ce qu'il peut faire |
|---|---|
| Grimpeur | Enregistrer ses séances, suivre sa progression, choisir les salles autorisées à consulter ses séances |
| Staff d'une salle | Consulter les informations de sa salle et les séances des grimpeurs qui l'ont autorisée |
| Direction | Consulter les statistiques de l'ensemble des salles |

## 2. Application mobile – grimpeurs

_Note : l'application mobile est en cours de transition d'un POC à une vraie implémentation de l'API et de l'authentification, la documentation arrivera ultérieurement quand les écrans seront vinalisés._

Écrans déjà réalisés :

| Accueil | Séances | Projets | Profil | Carnet |
|:-------:|:-------:|:-------:|:-------:|:-------:|
| <img width="200" alt="home" src="https://github.com/user-attachments/assets/c6fdec7a-63c9-48c2-9673-6b5fc7fdbe7f" /> | <img width="200" alt="seances" src="https://github.com/user-attachments/assets/9e2b2a0a-49b6-4728-8f73-9a1499885796" /> | <img width="200" alt="projet" src="https://github.com/user-attachments/assets/e412204b-e927-45a9-acd9-fea08245c4d5" /> | <img width="200" alt="profil" src="https://github.com/user-attachments/assets/4f163d0c-cc0f-4570-81aa-b3312009b331" /> | <img width="200" alt="carnet" src="https://github.com/user-attachments/assets/06d36f4b-42bb-4be8-b2d4-a0d7e192eee9" /> |


### 2.1 Parcours principal

> **À compléter (Front)** 

### 2.2 Enregistrer une séance

> **À compléter (Front)**

### 2.3 Suivre sa progression

> **À compléter (Front)**

### 2.4 Choisir les salles autorisées à consulter ses séances

Dans l'application, l'utilisateur peut sélectionner les salles autorisées à consulter ses séances afin de recevoir un suivi d'entraînement personnalisé.
Une salle non sélectionnée n'a pas accès à ses séances.

> **À compléter (Front)**

### 2.5 Gérer son compte

> **À compléter (Front)**

## 3. Backoffice – staff et direction

Le backoffice est une interface web accessible à l'adresse `/admin` du serveur MCL, avec un compte fourni par l'administrateur.

### 3.1 Ce que chaque rôle voit

| Rôle | Accès |
|---|---|
| Staff | Sa salle, et les séances et grimpes des utilisateurs ayant autorisé sa salle |
| Direction | Toutes les données |
| Grimpeur | Aucun accès au backoffice |

> Le périmètre exact est en attente de validation par le client.

### 3.2 Gérer les salles et les ouvertures

> À compléter quand la fonctionnalité sera disponible.

### 3.3 Consulter les séances des grimpeurs

> À compléter quand la fonctionnalité sera disponible.

### 3.4 Consulter les statistiques

> À compléter quand la fonctionnalité sera disponible.

## 4. Questions fréquentes

| Question | Réponse |
|---|---|
| Je n'arrive pas à me connecter | *À compléter* |
| Une salle ne voit pas mes séances | Vérifier que la salle fait partie de vos salles autorisées |
| *Autre question* | |

## 5. Obtenir de l'aide

> À compléter : contact de support (équipe projet ou Altissimo).

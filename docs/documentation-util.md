# Documentation utilisateur – MyClimbingList

*Dernière mise à jour : 25/11/2026 – Version : 0.1*

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

### 2.1 Parcours principal

> **À compléter (Front)** : décrire le parcours nominal.
>
> 1. Se connecter
> 2. Choisir une salle
> 3. Enregistrer une séance et les voies grimpées
> 4. Consulter son carnet et sa progression

### 2.2 Enregistrer une séance

> **À compléter (Front)** : étapes, captures d'écran, signification des champs (type de voie, statut, etc.).

### 2.3 Suivre sa progression

> **À compléter (Front)** : où trouver les statistiques, comment les lire.

### 2.4 Choisir les salles autorisées à consulter ses séances

Dans l'application, l'utilisateur peut sélectionner les salles autorisées à consulter ses séances afin de recevoir un suivi d'entraînement personnalisé.
Une salle non sélectionnée n'a pas accès à ses séances.

> **À compléter (Front)** : où se trouve ce réglage et comment le modifier.
> À confirmer avec l'équipe : le libellé exact dans l'application.

### 2.5 Gérer son compte

> **À compléter (Front)** : modifier son profil, changer ou réinitialiser son mot de passe, se déconnecter.

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

> À compléter : créer ou modifier une salle, ajouter une ouverture (voie ou bloc), changer son statut. Captures d'écran.

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

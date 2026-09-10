# Compte-rendu de réunion — My Climbing List (MCL)

**Participants :** Fabrice PELLEAU, Pierre PUGLIESI-CONTI, Olivier MARINX, Ethan JOUSSEIN, Rayan SABOUN, Axel MOYANO et Eliot OLIVENCIA

**Sujet :** Etablir un premier contact avec le client, cadrer les objectifs du projet et présentation de l'application par Pierre

**Date :** 09/09/2026

**Lieu :** Visioconférence en salle de réunion à l'IUT de Blagnac

---
 
## 1. Contexte et état de l'existant
 
- L'application actuelle est en développement depuis **2 ans**.
- Développée de manière **instinctive** par Pierre, un grimpeur autodidacte, sans formation initiale de développeur.
- Le **fonctionnel et l'ergonomie** sont satisfaisants pour les utilisateurs.
- Au fil du temps, les fonctionnalités se sont **empilées**, rendant les évolutions/maintenances de plus en plus difficiles.
- Une base de données existe mais nécessite d'être **remise à plat**.
- **Aucun choix technique n'est imposé** par le client : une **redéfinition/redéveloppement complet** est envisagée comme la meilleure option.
- Si besoin d'une API REST, possibilité de s'appuyer sur la base de données d'origine.
- L'application actuelle **ne tourne pas correctement sur tous les terminaux mobiles** :
  - Fonctionne : Samsung, iOS
  - Ne fonctionne pas : la majorité des terminaux Android (notamment les moins récents)
- Reste ouvert : rester en **webapp** ou évoluer vers une **application native/mobile**. Le client souhaite en priorité **du mobile**. 
---
 
## 2. Besoins et attentes du client
 
- Besoin que l'application puisse **continuer à être développée par d'autres développeurs** dans le futur (maintenabilité, documentation).
- **Idée directrice du produit :** MCL n'est **pas un réseau social**, mais un **outil d'entraînement et de gestion de contests**.
- Comparaison faite avec **Strava**, mais adapté au réseau de salles Altissimo, avec une dimension sociale réduite.
- **Oblique** est cité comme application similaire, plutôt orientée escalade extérieure.
- Deux usages principaux à couvrir :
  - **Entraînement** (usage courant)
  - **Concours / contests** (usage jugé **très important**)
- Livrables attendus :
  - Mise à plat complète du projet
  - Cahier des charges complet
  - Plan de développement complet
  - Base d'un manuel utilisateur
  - Phase de test de plusieurs choix technologiques envisagés (**Flutter, Webapp...**)
---
 
## 3. Présentation fonctionnelle de l'application actuelle
 
### 3.1 Authentification
- Page de connexion : création de compte, changement de mot de passe, contact support.
### 3.2 Carnet de voies (cœur de l'app)
- Objectif : servir de **carnet de croix numérique** = enregistrer les voies réalisées au cours d'une séance.
- Sélection de la salle (au sein du réseau Altissimo), puis sélection des voies faites pour les ajouter au carnet.
- Pour chaque voie : indication de réussite ou non, nombre d'essais, nombre de réussites.
- Notion de **"flash"** = réussite au premier essai (possible de flasher même en cas d'échec sur les essais suivants).
- Possibilité d'enregistrer une séance puis de la consulter a posteriori.
- Génération de **graphes de progression** : histogramme, graphe en araignée (radar).
### 3.3 Écrans principaux
- **Accueil** : résumé des séances, avec aperçu de la semaine en haut de page.
- **Profil** : accès au carnet complet (liste de toutes les voies faites, possibilité de laisser un avis).
- **Données personnelles** : username, nom, prénom, genre (donnée jugée importante pour les contests), suppression de compte (fonctionnalité nécessaire).
### 3.4 Projets (voies en cours)
- Une voie "essayée mais non réussie" peut être enregistrée comme **projet**.
- Possibilité de supprimer un projet.
### 3.5 Fonctionnalités complémentaires
- Mise en favori d'une salle.
- Depuis "ajouter une voie", accès direct aux voies de la salle sélectionnée (demande utilisateur explicite).
- Pour supprimer une séance : nécessité de supprimer d'abord toutes les voies associées.
- Icône indiquant si une voie a déjà été réalisée.
- Filtres sur les voies (ex. : uniquement celles flashées, etc.).
- Support multilingue : anglais, espagnol, portugais.
### 3.6 Système de niveau (ELO)
- Association entre un système type **ELO** et le niveau d'escalade.
- Principe : le niveau de départ du grimpeur (ex. 5c) est comparé au niveau de la voie tentée (ex. 6c).
- Réussir ou rater la voie fait évoluer l'ELO du grimpeur ; l'**ELO de la voie reste fixe**.
- Système asymétrique : on perd **3 fois moins d'ELO qu'on en gagne** (1 victoire ≈ 3 défaites).
---
 
## 4. Partie "Staff" / back-office
 
- Gestion des salles, création de compétitions, consultation de la fréquentation — via l'application elle-même.
- Deux niveaux d'administration : **Admin Staff** et **Admin Direction**.
---
 
## 5. Module Contest
 
- Formulaire dédié à la création d'un contest.
- Accessible depuis l'application, dans une partie **Contest** dédiée.
- L'utilisateur voit la liste des contests disponibles puis choisit sa salle/son évènement.
- Le module Contest **ne communique pas** avec la partie principale de l'application (carnet/entraînement).
  - Génère une certaine duplication de code/logique.
  - Choix conceptuellement plus simple car les rôles utilisateurs diffèrent entre les deux contextes.
- Fonctionnement : l'utilisateur coche les voies réussies ; objectif = établir un **classement** (pas de statistiques poussées ici, contrairement au carnet d'entraînement).
- **Cas des events par équipe** : existant en théorie mais insuffisamment testé. Difficultés identifiées :
  - Gestion des cas de "quack" (égalités/doublons de points à éviter).
  - Méthode de comptage des points complexe.
---
 
## 6. Architecture technique actuelle
 
- Backend : **Django** (aucune obligation de le conserver).
- Frontend : JavaScript généré via un outil/lib, reste globalement basique.
- **Guidebook** = module listant l'ensemble des voies disponibles.
- Remarque technique : il serait plus pertinent de séparer dans un module dédié les pages qui exploitent/affichent les données (actuellement mélangées avec le reste).
### 6.1 Gestion du cache
- Usage important du cache côté client.
- Réflexion en cours sur la stratégie d'invalidation/rafraîchissement du cache :
  - Avantage recherché : rapidité + fonctionnement **hors ligne**.
  - Chaque requête réseau interroge d'abord le cache.
  - Une page entière peut être mise en cache.
  - Une fois toutes les pages chargées, l'application peut fonctionner sans réseau.
  - Enregistrer une nouvelle voie déclenche une requête réseau et **réinitialise le cache** concerné.
 

# Compte-rendu de réunion — My Climbing List (MCL)

**Participants :** Fabrice PELLEAU, Ethan JOUSSEIN, Rayan SABOUN et Axel MOYANO

**Absents :** Eliot OLIVENCIA

**Sujet :** Point sur la situation, questions

**Date :** 16/09/2026

**Lieu :** Bureau de Fabrice

---
 
## 1. Objectifs pour la fin de semaine
 
- Disposer d'une **version locale fonctionnelle** de l'application.
- Pouvoir **consulter la base de données**.

---
 
## 2. Back-office / Administration
 
- Un **espace admin (back-office)** est requis.
- Clarification sur la hiérarchie : l'**admin Direction est au-dessus de l'admin Staff** (contrairement à l'état actuel de l'application).

---
 
## 3. Données et RGPD
 
- Les données collectées par l'application ne doivent collecter que le strict nécessaire.

---
 
## 4. Ergonomie et back-end
 
- L'**ergonomie et le style visuel actuels doivent être conservés**.
- Le **back-end peut en revanche être entièrement revu**.

---
 
## 5. POC et architecture technique
 
- Un **POC en webapp** pourrait être une bonne option pour valider rapidement les choix (webapp ou Flutter).
- Sécuriser un **back-end propre avec une API REST** serait utile pour faciliter la reprise par une future équipe de développeurs.
- Base de données actuelle : **PostgreSQL**. Piste envisagée pour la suite : **MySQL**, jugée préférable.
- Réflexion sur **Flutter** pour le développement mobile :
  - **Avantages** : structure du framework, facilité de déploiement.
  - **Inconvénients** : compétence moins répandue, ce qui pourrait compliquer la reprise du projet par une future équipe.
  
---
 
## 6. Déploiement
 
- Le sujet du **déploiement (et des licences associées)** doit être traité **dès le premier POC**, avec un déploiement immédiat plutôt que reporté en fin de projet (à rajouter dans CDC).
- Question technique à trancher : **comment compiler pour iOS ?** (ex. via GitHub Actions ou un service cloud de build).
- Il faut déterminer le **cadre fonctionnel minimal** nécessaire pour permettre un premier déploiement.

---
 
## 7. Priorisation fonctionnelle
 
- Fonctionnalités prioritaires : **l'intégralité des fonctionnalités côté client** de l'application (carnet de voies, séances, etc.), le back-office et les statistiques venant en complément.
- **Priorité n°1 : l'enregistrement des informations** (séances, voies, résultats).
- Piste technique évoquée : mettre en place une **table intermédiaire** qui précalculerait les données du carnet de croix pour les statistiques, plutôt que de tout recalculer à partir des données brutes à chaque fois. 
Objectif : alléger le système à long terme. Reste à vérifier si l'ensemble des données brutes est réellement nécessaire pour tracer les graphes de progression.
- Certaines **fonctionnalités non présentées** lors du recueil de besoin existent probablement dans l'application actuelle : c'est à l'équipe de juger de leur importance et de décider de les intégrer ou non.
- Le CDC doit contenir une **liste détaillée des fonctionnalités**, incluant à la fois celles déjà spécifiées et celles présentes dans l'application existante mais non encore traitées ailleurs dans le document.

---
 
## 8. Stratégie de pré-déploiement
 
- Le **pré-déploiement** est une étape clé du projet.
- Objectif : identifier les fonctionnalités **rapidement atteignables** pour pouvoir tester le déploiement au plus tôt, plutôt que d'attendre une version complète.

---
 
## 9. Point de vigilance
 
- Se méfier des **informations liées aux salles** (plans, descriptions) : fiabilité/qualité de ces données à vérifier avant de les intégrer telles quelles.

---
 
## 10. Échéances
 
- **Preview du CDC pour Fabrice** : fin de semaine.
- **Prochaine réunion** : jeudi prochain, 8h15.

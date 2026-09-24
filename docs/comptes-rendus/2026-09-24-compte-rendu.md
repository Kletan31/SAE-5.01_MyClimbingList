# Compte-rendu de réunion — My Climbing List (MCL)

**Participants :** Fabrice PELLEAU, Ethan JOUSSEIN, Rayan SABOUN, Axel MOYANO et Eliot OLIVENCIA

**Absents :** Aucun

**Sujet :** Point sur le CdC et le travail effectué

**Date :** 24/09/2026

**Lieu :** Bureau de Fabrice

---
 
## 1. Base de données existante et migration
 
- Aucune information claire ne permet de confirmer si la base de données actuellement à disposition (vide) correspond bien à la **vraie base de production**.
- Certaines tables vides dans la version étudiantes seraient-elles vides également dans la vraie ? Ou seulement vides car contenant des données confidentielles ?
- Le manquement de data sera important pour la **phase de migration**.
- Il serait utile d'obtenir la **structure de la vraie base de données** (schéma), même sans les données elles-mêmes.
- **Démarche retenue** : récupérer la base existante > refaire le schéma > poser le backend dessus > développer l'API REST.
  
---
 
## 2. Choix technologique backend
 
- **Django** : jugé peu intéressant
- **Symfony** : jugé meilleur pour le projet, malgré l'absence d'expérience de l'équipe.
- Possibilité de faire un **petit tutoriel Symfony** pour monter en compétence.
- L'objectif principal est de pouvoir produire une simple **API REST**.
  
---
 
## 3. Interface back-office
 
- **Nécessité de développer une véritable interface back-office** : certaines fonctionnalités ne doivent pas être gérées depuis l'application Flutter.
- Outil envisagé pour le front de cet outil d'administration : **EasyAdmin**.
  
---
 
## 4. Répartition de l'équipe
 
- Répartition envisagée : **2 personnes fortes sur Symfony, 2 personnes fortes sur Flutter**.

---
 
## 5. POC Flutter - conseils techniques
 
- Lors de la présentation du début du POC, conseil donné :
  - Commencer par une **fausse API REST**.
  - Une **simulation en GET** est suffisante et simple à mettre en place pour démarrer.
---
 
## 6. Environnement de développement
 
- Le développement peut se faire **en local ou sur une VM**, au choix.

---
 
## 7. Licences, déploiement et chiffrage
 
- Points à clarifier : comment gérer les **licences iOS et Android** (comptes développeur, coûts associés).
- Comprendre concrètement **comment se déroule la publication sur iOS**.
- **Prévoir les coûts** associés à ces licences dans le cahier des charges.
-  **Le chiffrage dans le CDC est un point important**.

---
 
## 8. Échéances

- **Prochaine réunion** : mardi 29/09 à 14h.

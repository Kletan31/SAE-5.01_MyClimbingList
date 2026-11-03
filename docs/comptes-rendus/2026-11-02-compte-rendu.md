# Compte-rendu de réunion — My Climbing List (MCL)

**Participants :** Fabrice PELLEAU, Ethan JOUSSEIN, Rayan SABOUN, Axel MOYANO et Eliot OLIVENCIA

**Absents :** Aucun

**Sujet :** Point sur le travail effectué, tentative de résolutions de problèmes et questions éventuelles

**Date :** 02/11/2026

**Lieu :** Visioconférence

---

## 1. Suivi des actions précédentes

- Fabrice n'a pas eu le temps d'avancer sur les différents points qui lui avaient été confiés pendant les vacances.
- Le numéro **DUNS** a déjà été demandé par Altissimo, il n'est donc pas nécessaire d'effectuer une nouvelle demande.
- La procédure de création et de validation des comptes développeur reste bloquée en attente d'une réponse de Pierre.
- Dès réception du numéro DUNS et des informations associées, les éléments seront transmis à l'équipe.

---

## 2. Point sur les fonctionnalités

### Indication des nouvelles voies

- Dans l'application actuelle, certaines voies affichent un symbole en forme d'étoile.
- Cette étoile indique qu'il s'agit d'une **nouvelle voie récemment ouverte dans la salle**.
- Cette fonctionnalité est jugée pertinente et pourrait être conservée dans la nouvelle application.
- Proposition retenue : considérer une voie comme "nouvelle" pendant une durée d'environ **une semaine** après sa création.

### Consultation des caractéristiques des voies

- Fabrice partagera un lien permettant de consulter les caractéristiques détaillées des voies.

### Voies flashables

- Certaines voies ne sont actuellement pas flashables dans l'application historique.
- Ce comportement est considéré comme un bug de l'ancienne application.
- Dans la nouvelle version, **toutes les voies devront être flashables**.

---

## 3. Base de données et migration

- La base de données historique n'est toujours pas disponible.
- La procédure permettant d'obtenir l'accès aux différents comptes reste bloquée tant qu'une réponse de Pierre n'a pas été obtenue.
- Le dump de la base de données sera transmis dès qu'il sera disponible.
- Le schéma de l'ancienne base reste utile afin de vérifier qu'aucune fonctionnalité importante n'a été oubliée lors de la conception.

---

## 4. Avancement du backend

- Le formulaire d'authentification du back-office est fonctionnel.
- La mise en place des **webservices avec authentification** est désormais une priorité afin de permettre l'avancement du frontend et de l'application mobile.
- L'équipe backend s'est renseignée sur **PHPUnit** et sur les pratiques de **TDD (Test Driven Development)**.
- Bien que certains enseignants semblent valoriser cette approche, elle n'est **pas obligatoire dans le cadre du projet**.

---

## 5. Échanges de ressources

Les éléments suivants seront transmis dès qu'ils seront disponibles :

- Le dump de la base de données historique.
- Le code JavaScript utilisé pour les cartes 2D.
- Le lien de consultation des caractéristiques des voies.
  
---
 
## 6. Échéances

- **Si DUNS obtenu avant** : mercredi 4/11 à 8h15 en distanciel.
- **Prochaine réunion physique** : jeudi 12/11 à 8h30.

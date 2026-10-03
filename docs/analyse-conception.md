# Document d'analyse et de conception
## Refonte de l'application My Climbing List (MCL)

**Équipe :** Ethan JOUSSEIN, Elliot OLIVENCIA, Rayan SABOUN, Axel MOYANO

**Client :** Altissimo

---

# Partie 1 — Analyse

## 1.1 Contexte

Altissimo est une entreprise française créée en 1995 à Toulouse (SARL, siège à Montaudran), exploitant un réseau de plus de 10 salles d'escalade en France ainsi qu'une salle à Lisbonne. 
Au-delà de la gestion de ses salles, elle construit ses propres murs/structures d'escalade et fabrique ses prises et volumes.

L'application **My Climbing List** sert de carnet de progression numérique pour les grimpeurs du réseau et d'outil d'organisation de contests. 
L'application actuelle, développée en interne de façon instinctive, fonctionne bien sur le plan ergonomique mais souffre de limites techniques (base de données peu structurée, logique métier empilée, compatibilité mobile partielle) qui justifient une refonte complète plutôt qu'une simple maintenance évolutive.

## 1.2 Objectifs du projet

- **Côté client (Altissimo) :** améliorer les performances de l'application, faciliter sa reprise par de futures équipes de développeurs, migrer vers une application mobile native (meilleure intégration système, installation via stores, compatibilité élargie), tout en conservant au maximum les fonctionnalités existantes et en simplifiant l'ajout d'événements et le déploiement de correctifs.
- **Côté développeurs :** réécrire le backend pour exposer une API REST, réécrire le frontend pour un déploiement sur Android et iOS, et documenter l'ensemble (base de données, API, architecture, RGPD, authentification).

## 1.3 Attentes client

- Compatibilité Android 7.0 et supérieur.
- Code clair et bien organisé pour faciliter la reprise.
- Création d'événements simplifiée, sans modification du backend.
- Mode hors ligne : consultation seule des données déjà chargées (la saisie d'une séance nécessite une connexion).
- Migration des données validée par script de comparaison entre l'ancienne et la nouvelle base.

## 1.4 Public cible

- **Utilisateurs standard (grimpeurs) :** accès via application mobile, avec une ergonomie transparente par rapport à l'existant et de meilleures performances (chargement, hors ligne, synchronisation).
- **Administrateurs :** deux profils, staff et direction (la direction hérite des droits du staff), avec accès via un tableau de bord web dédié et cloisonné.

## 1.5 Fonctionnalités principales (synthèse)

| Fonction | Rôle |
|---|---|
| Topo | Catalogue des ouvertures par salle, triées par relais/niveau, avec badges de réussite |
| Saisie d'une séance | Enregistrement rapide de la pratique (essais, tops, flash) |
| Carnet | Agrégation des réalisations par ouverture (historique, filtres flash/tête) |
| Projets | Suivi des ouvertures tentées non encore réussies |
| Statistiques | Graphiques de volume et de diversité de pratique |
| Progression / niveau | Système Elo adapté (bloc/voie séparés) |
| Gestion des salles | Référentiel des salles, salle favorite |
| Staff | Suivi des grimpeurs, gestion de contests, exports |
| Direction | Dashboards de fréquentation et de rétention réseau |
| Contests | Compétitions liées au compte MCL, classements |
| Événements bloc | Compétitions en duo, classement par points/zones |
| Événements voie | Compétitions individuelles multi-voies, classement par moyenne géométrique des rangs |
| Alti Ligue | Classement réseau quotidien basé sur l'Elo |

Chaque fonction fait l'objet, dans le Cahier des charges, d'une description détaillée de son comportement attendu et des limites à corriger lors de la refonte.

## 1.6 Conformité réglementaire

L'application traite des données personnelles (compte, profil, performances) et est donc soumise au RGPD : politique de confidentialité, consentement explicite, droit à l'effacement, portabilité, minimisation des données, durée de conservation définie, droits d'accès/rectification/opposition, notification CNIL sous 72h en cas de violation.

Côté sécurité : mots de passe hachés, HTTPS obligatoire, protection contre les vulnérabilités web/API courantes (injections, XSS), stockage sécurisé côté mobile (Keychain/Keystore), limitation des tentatives de connexion, expiration des sessions, chiffrement des données sensibles, veille sur les dépendances, sauvegardes régulières.

## 1.7 Contraintes budgétaires et délais

Projet pédagogique sans budget réel (coût de main-d'œuvre théorique soit environ 7 680 € brut sur 128h × 4 développeurs). Coûts réels à prévoir : licences développeur Apple (99 $/an) et Google Play (25 $, unique), au nom d'Altissimo. CI GitHub avec 2 000 minutes de compilation, à réévaluer après le Sprint 1.

Projet mené en SCRUM du 1er septembre 2026 au 22 janvier 2027, sur 5 sprints (Sprint 0 à Sprint 4), avec une priorisation des fonctionnalités en 3 niveaux répartie sur les sprints.

---

# Partie 2 — Conception

## 2.1 Choix d'architecture générale

```
[ App mobile Flutter ]   [ Back-office web (EasyAdmin) ]
            \                      /
             \                    /
              [   API REST (Symfony)   ]
                        |
              [ Base de données MySQL ]
```

## 2.2 Backend — Symfony

Le choix s'est porté sur **Symfony** plutôt que sur la reconduction de Django (utilisé par l'application actuelle), pour plusieurs raisons :

- Symfony est structuré autour de composants découplés et d'une architecture orientée services, ce qui facilite la production d'une API REST propre, contrairement à l'application actuelle où logique métier et génération de pages HTML sont mélangées.
- Son système de validation et de sérialisation permet de corriger la validation actuellement faite côté JavaScript et insuffisamment reprise côté serveur.
- Compatible avec l'objectif de limiter le traitement serveur au strict nécessaire.

## 2.3 Back-office — EasyAdmin

Certaines fonctionnalités (gestion des salles, création de contests, consultation de la fréquentation, modération) ne doivent pas transiter par l'application mobile. **EasyAdmin**, bundle Symfony dédié à la génération rapide d'interfaces d'administration, est utilisé pour construire ce tableau de bord web staff/direction, avec un cloisonnement des droits par rôle (staff vs direction).

## 2.4 Base de données — MySQL

La base actuelle est en PostgreSQL. **MySQL** est retenue pour la nouvelle base et le schéma sera reconstruit de zéro (plutôt que migré tel quel).

## 2.5 Mobile — Flutter

**Flutter** a été choisi pour le développement de l'application mobile native (Android/iOS) :

**Avantages retenus :**
- Un seul code source pour les deux plateformes, cohérent avec une équipe réduite et un calendrier contraint.
- Structuration par widgets qui facilite un déploiement rapide sur les stores dès les premiers sprints.
- Écosystème de bibliothèques pour le hors ligne (cache local), les graphiques (statistiques, progression) et l'appel à une API REST.

**Limite assumée :** Flutter est une compétence moins répandue, ce qui pourrait complexifier la reprise du projet par une future équipe de développeur. Le projet sera donc documenté particulièrement soigneusement pour compenser ce risque.

### Application native vs web app

Le choix d'une application native plutôt que de la conservation d'une web app répond à plusieurs attentes exprimées par le client :

| Critère | Web app (actuelle) | App native (Flutter) |
|---|---|---|
| Installation | Dépend du navigateur, pas de présence sur les stores | Installation standard via Play Store / App Store |
| Performances | Dépend du moteur du navigateur mobile | Compilée, plus réactive |
| Compatibilité terminaux | Hétérogène (l'appli actuelle ne fonctionne pas sur une bonne partie des Android non-Samsung) | Compatibilité large validée dès le développement (cible Android 7.0+) |
| Visibilité / confiance utilisateur | Moindre, pas d'affichage dans les stores | Plus grande visibilité |

Ce choix implique en contrepartie une gestion des licences développeur (Apple/Google) et de la compilation iOS, pour laquelle le projet s'appuie sur une CI GitHub Actions et un accès physique à un Mac pour les premières compilations.

*Ces choix seront validés techniquement lors de la phase de POC du Sprint 1.*

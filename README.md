# SAE-5.01_MyClimbingList

## Description

My Climbing List (MCL) est une application développée pour le réseau de salles d'escalade Altissimo.
Elle permet notamment aux grimpeurs de sauvegarder leurs séances et de suivre leur progression.
La direction et le staff d'Altissimo peuvent également consulter les statistiques de leurs salles et organiser plus facilement leurs contests.

Une première version a déjà été réalisée sous forme de WebApp (Django, PostgreSQL et HTML/CSS/JS) par un grimpeur volontaire.
Ce dernier ne pouvant continuer le développement, le projet est repris par notre équipe étudiante de 3e année de BUT Informatique à l'IUT de Blagnac.

Nos objectifs sont :
1. Analyser l'existant pour créer un cahier des charges et cadrer les fonctionnalités de MCL ;
2. Refactorer l'application en conservant son apparence pour la transformer en application mobile (Symfony, MySQL et Flutter) disponible sur les stores ;
3. Rédiger des documentations pour les éventuels futurs développeurs qui reprendront le projet.

## Équipe

| Rôle | Nom |
|---|---|
| Scrum Master | Ethan JOUSSEIN |
| Product Owner | Axel MOYANO |
| Développeur | Rayan SABOUN |
| Développeur | Eliot OLIVENCIA |

## Client

- **Société** : Altissimo
- **Intermédiaire client** : Fabrice PELLEAU

## Organisation du projet

### Planning de télétravail

*Dernière mise à jour : 25/11/2026*
 
| Date | Heure de début | Heure de fin |
|---|---|---|
| 15/09/2026 | 14:15 | 17:15 |
| 17/09/2026 | 9:30 | 12:30 |
| 21/09/2026 | 14:15 | 17:15 |
| 08/10/2026 | 8:00 | 11:00 |
| 16/10/2026 | 9:30 | 12:30 |
| 10/11/2026 | 14:15 | 17:15 |
| 16/11/2026 | 14:15 | 17:15 |

### Chiffrage du projet

*Dernière mise à jour : 25/11/2026*
 
**Commits par membre**
 
| Membre | Nombre de commits |
|---|---|
| Ethan JOUSSEIN | 42 |
| Axel MOYANO | 70 |
| Rayan SABOUN | 35 |
| Eliot OLIVENCIA | 7 |
| **Total** | **154** |

**Temps de travail et réunions**
 
| Indicateur | Valeur |
|---|---|
| Heures de créneau de travail de l'équipe | +120 h |
| Réunions avec le client | 7 |

**Chiffrage financier**

Disponible dans [docs/chiffrage.md](./docs/chiffrage.md).

## Livrables attendus

*Dernière mise à jour : 25/11/2026*
 
| Livrable | Description | État | Lien |
|---|---|---|---|
| Cahier des charges | Fonctionnalités de MCL cadrées à partir de l'analyse de l'existant | Livré | [docs/cahier-des-charges](./docs/cahier-des-charges) |
| Analyse & conception | Analyse de l'existant, conception de l'application | Livré | [docs/analyse-conception.md](./docs/analyse-conception.md) |
| Backend (API et base de données) | API Symfony et base MySQL | En cours | [backend/](./backend) |
| Application mobile | Application Flutter, disponible sur les stores | En cours | [frontend/](./frontend) |
| Documentation du code | Documentation à destination des futurs développeurs | En cours | [docs/documentation-code.md](./docs/documentation-code.md) |
| Documentation utilisateur | Guide d'utilisation de l'application | En cours | [docs/documentation-util.md](./docs/documentation-util.md) |
| Documentation administrateur | Guide d'administration (backoffice, déploiement) | En cours | [docs/documentation-admin.md](./docs/documentation-admin.md) |
| Cahier de recette | Cas de test versionnés et leurs résultats | En cours | [docs/cahier-de-recette.md](./docs/cahier-de-recette.md) |
| Releases | Versions livrées, avec notes de release commentées | En cours | [Releases](../../releases) |
| Chiffrage | Coût du projet s'il était réalisé par une équipe de professionnel | Livré | [docs/chiffrage.md](./docs/chiffrage.md) |

## Documentation

La documentation est versionnée dans le dossier [`docs/`](./docs) :
- [Comptes-rendus de réunion](./docs/comptes-rendus)
- [Cahiers des charges](./docs/cahier-des-charges)
- [Informations licences de développement](./docs/MCL-informations-licences-dev.pdf)
- [Analyse & conception](./docs/analyse-conception.md)
- [Réflexions de conception pour le Backend](./docs/backend)
- [Documentation du code](./docs/documentation-code.md)
- [Documentation utilisateur](./docs/documentation-util.md)
- [Documentation administrateur](./docs/documentation-admin.md)
- [Cahier de recette](./docs/cahier-de-recette.md)
- [Chiffrage financier](./docs/chiffrage.md)

Le client ne nécessite pas toutes ces documentations.
Nous les réalisons néanmoins, car elles font partie des attendus pédagogiques de la SAE et sont évaluées.
Elles serviront aussi aux futurs développeurs qui reprendront le projet.

## Tests

Le client n'a pas demandé de tests.
Nous en réalisons néanmoins, car l'équipe enseignante les attend :
- un cahier de recette versionné dans `docs/` ;
- des tests automatisés seront par la suite exécutés par la pipeline GitHub Actions.

## Présence de l'IA dans les commits GitHub

Copilot a été utilisé temporairement pour corriger la configuration d'une GitHub Action après l'échec du runner.
L'IA n'a généré aucun code ni aucune fonctionnalité dans le projet.

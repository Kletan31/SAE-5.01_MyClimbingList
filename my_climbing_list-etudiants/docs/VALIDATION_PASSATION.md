# Validation de passation

## Version testée

Commit : `04bf7f01a7da58ecd3ffecc34e42b4a1bafc9d13`.

La recette finale du 13 septembre 2026 a été réalisée depuis une copie créée exclusivement à partir du contenu versionné, via `git archive HEAD`. Ce compte rendu consigne la recette achevée ; la finalisation du paquet est uniquement documentaire.

## Environnement validé

Docker Desktop / Docker Compose, PostgreSQL local Docker, Django, nginx et HTTPS local avec mkcert. Test effectué sur macOS avec Safari. Windows, Linux et Firefox n'ont pas été directement validés lors de cette recette.

## Installation

Validés : création de `.env` depuis `.env.example`, génération des certificats locaux, build Docker, PostgreSQL, initialisation, création du schéma, seed synthétique, Django, nginx, HTTPS et connexion avec le compte de démonstration.

## Données synthétiques après reset

- 3 salles ;
- 18 ouvertures ;
- 2 comptes ;
- 19 pratiques.

## Parcours fonctionnels validés

Salle voie, salle bloc, topo liste / plan, saisie d'une pratique, carnet / historique et projets.

## Écriture testée

Pratique créée depuis l'interface :

- compte : `demo.climb` ;
- salle : Démo Voie ;
- ouverture : Nuage violet ;
- emplacement : Relais 3 ;
- cotation / couleur : 6c / Mauve ;
- date : 13 septembre 2026 ;
- moulinette : 4 essais, 1 top ;
- tête : 0 essai, 0 top ;
- flash : non.

## Persistance

PERSISTANCE VALIDÉE

Seul le service web a été redémarré. La pratique était toujours présente après redémarrage.

## Reset

RESET VALIDÉ

Seul le volume du projet de test a été supprimé. PostgreSQL a été reconstruit, le schéma recréé et le seed rejoué. La pratique créée pendant la recette avait disparu ; les données synthétiques initiales étaient revenues.

## Documentation

Parcours documentaire jugé naturel ; `MCL_COMPRENDRE.md` validé ; PDF validé (15 pages) ; DOCX validé et modifiable ; illustrations présentes. La compréhension métier a été jugée suffisante : aucune lecture du code métier n'a été nécessaire pour comprendre et lancer le projet.

## Sécurité

Aucun secret réel nécessaire ou découvert pendant la recette ; aucune donnée personnelle réelle découverte dans les éléments examinés ; aucun accès production nécessaire ou effectué ; aucun certificat historique utilisé. Les certificats de test ont été générés localement. Ces constats portent sur les éléments examinés et ne constituent pas un audit de sécurité exhaustif.

## Limites connues de la démonstration

1. Les indicateurs du profil peuvent rester à zéro top / zéro flash malgré les réalisations synthétiques du carnet.
2. Après changement vers Démo Bloc, il peut être nécessaire de cliquer sur « Bloc » pour faire apparaître les ouvertures.

Ces deux comportements sont des réserves non bloquantes conservées dans le POC et n'empêchent pas la reprise du projet.

Conformément au guide étudiant, Staff et Direction n'ont pas de parcours de démonstration préparé ; Contest n'a pas de démonstration complète. Elo/progression ne constitue pas un parcours de démonstration complet : les calculs ne sont pas exécutés automatiquement au démarrage.

## Verdict

PASSATION ÉTUDIANTE VALIDÉE

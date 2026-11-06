# Conception Base de données V3

Les tables traitant de l'elo, des projets, des contests et des évènements ne sont pas encore présentes dans cette version.

## Relations

- Salle 1:N Ouverture
- Salle 1:N Seance
- Utilisateur 1:N Seance
- Seance 1:N Grimpe
- Ouverture 1:N Grimpe
- Utilisateur N:N Salle via Suivi
- Utilisateur 0:1 Salle favorite

## Tables

### Salle

Une salle d'escalade Altissimo

| Attribut                     | Type                  | Nullable | Description                    |
|------------------------------|-----------------------|----------|--------------------------------|
| id                           | INT PK AUTO_INCREMENT | Non      | Identifiant                    |
| nom                          | VARCHAR(100)          | Non      | Nom                            |
| ville                        | VARCHAR(100)          | Oui      | Ville                          |
| pays                         | VARCHAR(2)            | Oui      | Code pays ISO                  |
| masquer_cotations_recentes   | BOOLEAN               | Non      | Masquer cotations récentes     |
| image                        | VARCHAR(255)          | Oui      | Nom de l'image ou URL          |

A clarifier : stockage des images. 

### Utilisateur

Un utilisateur de MCL

| Attribut             | Type                  | Nullable | Description                           |
|----------------------|-----------------------|----------|---------------------------------------|
| id                   | INT PK AUTO_INCREMENT | Non      | Identifiant                           |
| nom                  | VARCHAR(100)          | Oui      | Nom                                   |
| prenom               | VARCHAR(100)          | Oui      | Prénom                                |
| nom_utilisateur      | VARCHAR(50) UNIQUE    | Non      | Pseudonyme                            |
| email                | VARCHAR(180) UNIQUE   | Non      | Identifiant connexion                 |
| password             | VARCHAR(255)          | Non      | Hash du mot de passe                  |
| genre                | VARCHAR(1)            | Oui      | Genre                                 |
| langue               | VARCHAR(5)            | Non      | Langue, ex. fr                        |
| date_inscription     | DATETIME              | Non      | Inscription                           |
| salle_favorite_id    | INT FK Salle(id)      | Oui      | Salle favorite                        |
| roles                | JSON                  | Non      | Rôle                                  |

A voir pour les salles que la staff peut gérer.

### Ouverture

Bloc ou voie d'escalade

| Attribut        | Type               | Nullable | Description                               |
|-----------------|--------------------|----------|-------------------------------------------|
| id              | INT PK AUTO_INCREMENT | Non   | Identifiant                               |
| salle_id        | INT FK Salle(id)   | Non      | Salle propriétaire                        |
| type            | VARCHAR(5)         | Non      | bloc, voie…                               |
| cotation        | VARCHAR(50)        | Non      | Cotation                                  |
| couleur         | VARCHAR(50)        | Oui      | Couleur textuelle                         |
| couleur_hex     | VARCHAR(11)        | Oui      | Code hex                                  |
| date_creation   | DATE               | Non      | Création / ouverture                      |
| relais          | INT                | Oui      | Numéro d'identification du relais         |
| secteur         | VARCHAR(100)       | Oui      | Secteur                                   |
| statut          | VARCHAR(10)        | Non      | État                                      |
| date_demontage  | DATE               | Oui      | Démontage                                 |
| en_tete         | BOOLEAN            | Non      | Indique si la voie peut être fait en tête |
| proprietes      | JSON ?             | Oui      | A voir, tableau de liste de propriété ou une autre table |

Réflexion à confirmer avec dump de la BD existante : faire de propriétés 2 colonnes (profil et style), ça serait utile pour les statistiques.
en_tete en false par défaut, et tjrs faux pour un bloc.

### Séance

Séance d'escalade d'un utilisateur

| Attribut          | Type                     | Nullable | Description               |
|-------------------|--------------------------|----------|---------------------------|
| id                | INT PK AUTO_INCREMENT    | Non      | Identifiant               |
| utilisateur_id    | INT FK Utilisateur(id)   | Non      | Grimpeur                  |
| salle_id          | INT FK Salle(id)         | Non      | Salle de séance           |
| date_seance       | DATE                     | Non      | Date                      |
| cree_le           | DATETIME                 | Non      | Création                  |
| modifie_le        | DATETIME                 | Non      | Modification              |

Changement de la V3 : suppression Discipline (inutile car Type est dans Ligne) ; suppression clé antidoublon (suggérée par IA).
Unicité sur (utilisateur_id, salle_id, date_seance) pour éviter les doublons.

### Grimpe

Détail d'un des lignes grimpée dans une séance
Grimpe = ligne de pratique du CDC

| Attribut    | Type                | Nullable | Description                 |
|-------------|---------------------|----------|-----------------------------|
| id          | INT PK AUTO_INCREMENT | Non    | Identifiant                 |
| seance_id   | INT FK Seance(id)   | Non      | Séance                      |
| ouverture_id    | INT FK Ligne(id)    | Non  | Ouverture grimpée           |
| montee      | INT                 | Non      | Nombre de montées/essais    |
| top         | INT                 | Non      | Nombre de tops              |
| flash       | BOOLEAN             | Non      | Réussite au premier essai   |
| montee_tete | INT                 | Non      | Nombre de montées/essais (en tête) |
| top_tete    | INT                 | Non      | Nombre de tops (en tête)    |
| flash_tete  | BOOLEAN             | Non      | Réussite au premier essai (en tête) |
| cree_le     | DATETIME            | Non      | Création                    |
| modifie_le  | DATETIME            | Non      | Modification                |

Unicité sur (seance_id, ligne_id).
Stats de montées à 0/false par défaut.

### Suivi

Autorisations accordées à une salle pour consulter les séances d'un utilisateur

| Attribut        | Type                     | Nullable | Description            |
|-----------------|--------------------------|----------|------------------------|
| id              | INT PK AUTO_INCREMENT    | Non      | Identifiant            |
| utilisateur_id  | INT FK Utilisateur(id)   | Non      | Utilisateur suivi      |
| salle_id        | INT FK Salle(id)         | Non      | Salle autorisée        |
| cree_le         | DATETIME                 | Non      | Création autorisation  |

Unicité sur (utilisateur_id, salle_id).

## Points à clarifier

- Propriétés d'une ouverture.
- Règles de suppression.
- Staff peut gérer une seule salle (attribut) ou plusieurs (table de jointure) ?
- en_tete signifie-t-il "peut être faite en tête" ou "doit l’être" ?
- Direction : accès global autorisé selon ses permissions. 
- Staff : accès limité à sa salle et aux utilisateurs suivis par cette salle. 
- Utilisateur : accès à ses propres séances/grimpes.

## Hypothèses pour contests et évènements

contest(id (INT), nom (VARCHAR(255)), description_courte (VARCHAR(255)), description (TEXT), #salle_id (INT), discipline (VARCHAR(10)), format (VARCHAR(30)), date_debut (DATETIME), date_fin (DATETIME), #cree_par_id (INT), #contest_initial_id (INT), visible (BOOLEAN), payant (BOOLEAN), par_equipe (BOOLEAN), permanent (BOOLEAN), permanent_actif (BOOLEAN), avec_zone (BOOLEAN), avec_degaines (BOOLEAN), masquer_cotations (BOOLEAN), trier_par_nom (BOOLEAN), combine (BOOLEAN), max_participants (INT))

contest_ouverture(#contest_id (INT), #ouverture_id (INT))

contest_inscription(id (INT), #contest_id (INT), #utilisateur_id (INT), date_inscription (DATETIME), statut (VARCHAR(20)), score_initial (INT))

contest_resultat(id (INT), #contest_id (INT), #utilisateur_id (INT), #ouverture_id (INT), a_top (BOOLEAN), a_zone (BOOLEAN), degaines_atteintes (INT), cree_le (DATETIME))

contest_equipe(id (INT), #contest_id (INT), nom (VARCHAR(255)), cree_le (DATETIME), modifie_le (DATETIME))

contest_equipe_membre(#equipe_id (INT), #utilisateur_id (INT))

message_popup(id (INT), code (VARCHAR(50)), cree_le (DATETIME))

message_popup_traduction(id (INT), #popup_id (INT), langue (VARCHAR(5)), titre (VARCHAR(200)), contenu (TEXT))

message_popup_vue(id (INT), #utilisateur_id (INT), #popup_id (INT), vu_le (DATETIME))

evenement_bloc(id (INT), nom (VARCHAR(255)), slug (VARCHAR(255)), #salle_id (INT), date (DATE), cree_le (DATETIME))

evenement_bloc_phase(id (INT), #evenement_id (INT), nom (VARCHAR(100)), heure_debut (TIME), heure_fin (TIME), capacite (INT))

evenement_bloc_ouverture(id (INT), #evenement_id (INT), #ouverture_id (INT), points (INT), avec_zone (BOOLEAN), ordre_affichage (INT))

evenement_bloc_participant(id (INT), #evenement_id (INT), prenom (VARCHAR(100)), nom (VARCHAR(100)), email (VARCHAR(254)), genre (CHAR(1)), cree_le (DATETIME))

evenement_bloc_equipe(id (INT), #evenement_id (INT), #participant_1_id (INT), #participant_2_id (INT), #phase_id (INT), type_equipe (VARCHAR(20)), paiement_valide (BOOLEAN), jeton_acces (VARCHAR(64)), cree_le (DATETIME))

evenement_bloc_performance(id (INT), #participant_id (INT), #bloc_id (INT), top (BOOLEAN), zone (BOOLEAN), cree_le (DATETIME), modifie_le (DATETIME))

evenement_voie(id (INT), nom (VARCHAR(255)), slug (VARCHAR(255)), #salle_id (INT), date (DATE), cree_le (DATETIME))

evenement_voie_phase(id (INT), #evenement_id (INT), nom (VARCHAR(100)), heure_debut (TIME), heure_fin (TIME), capacite (INT))

evenement_voie_ouverture(id (INT), #evenement_id (INT), #ouverture_id (INT), ordre_affichage (INT))

evenement_voie_participant(id (INT), #evenement_id (INT), #phase_id (INT), prenom (VARCHAR(100)), nom (VARCHAR(100)), email (VARCHAR(254)), genre (CHAR(1)), paiement_valide (BOOLEAN), jeton_acces (VARCHAR(64)), cree_le (DATETIME))

evenement_voie_performance(id (INT), #participant_id (INT), #voie_id (INT), numero_prise (INT), prise_plus (BOOLEAN), cree_le (DATETIME), modifie_le (DATETIME))

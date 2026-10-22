# Conception Base de donnée 
utilisateur(id (INT), email (VARCHAR(180)), roles (JSON), password (VARCHAR(255)), nom (VARCHAR(100)), prenom (VARCHAR(100)), genre (VARCHAR(1)), langue (VARCHAR(5)), date_inscription (DATETIME), #salle_favorite_id (INT))

salle(id (INT), nom (VARCHAR(100)), ville (VARCHAR(100)), pays (VARCHAR(2)), masquer_cotations_recentes (BOOLEAN))

ouverture(id (INT), #salle_id (INT), discipline (VARCHAR(5)), relais (INT), cotation (VARCHAR(50)), couleur (VARCHAR(50)), couleur_hex (VARCHAR(11)), date_ouverture (DATE), statut (VARCHAR(10)), date_demontage (DATE))

seance(id (INT), #utilisateur_id (INT), #salle_id (INT), discipline (VARCHAR(5)), date_seance (DATE), cle_idempotence (VARCHAR(36)), cree_le (DATETIME), modifie_le (DATETIME))

ligne_pratique(id (INT), #seance_id (INT), #ouverture_id (INT), essais (INT), tops (INT), essais_tete (INT), tops_tete (INT), flash (BOOLEAN), flash_tete (BOOLEAN), cree_le (DATETIME), modifie_le (DATETIME))

**Hypothèses :**

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

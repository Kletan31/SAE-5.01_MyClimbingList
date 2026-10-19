import 'package:my_climbing_list_poc/models/contest_model.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/models/seance_model.dart';
import 'package:my_climbing_list_poc/models/suivi_model.dart';
import 'package:my_climbing_list_poc/models/user_model.dart';

abstract class ApiService {
  // Salles : GET/POST /salles, GET/PUT/DELETE /salles/{id}
  Future<List<Salle>> getSalles();
  Future<Salle?> getSalle(int id);
  Future<Salle> createSalle(Salle salle);
  Future<Salle> updateSalle(Salle salle);
  Future<void> deleteSalle(int id);

  // Lignes
  Future<List<Ligne>> getLignes({int? salleId, int? userId});
  Future<Ligne?> getLigne(int id);
  Future<Ligne> createLigne(Ligne ligne);
  Future<Ligne> updateLigne(Ligne ligne);
  Future<void> deleteLigne(int id);

  // Users
  Future<List<User>> getUsers();
  Future<User?> getUser(int id);
  Future<User> createUser(User user);
  Future<User> updateUser(User user);
  Future<void> deleteUser(int id);

  // Suivis (pas d'id : la clé est le couple utilisateur / salle)
  Future<List<Suivi>> getSuivis(int userId);
  Future<void> addSuivi(Suivi suivi);
  Future<void> removeSuivi(Suivi suivi);

  // Contests
  Future<List<Contest>> getContests();
  Future<Contest?> getContest(int id);
  Future<Contest> createContest(Contest contest);
  Future<Contest> updateContest(Contest contest);
  Future<void> deleteContest(int id);

  // Séances (clé : id_seance)
  Future<List<Seance>> getSeances({int? userId});
  Future<Seance?> getSeance(int id);
  Future<Seance> createSeance(Seance seance);
  Future<Seance> updateSeance(Seance seance);
  Future<void> deleteSeance(int id);

  // Grimpes (clé : id_grimpe)
  Future<List<Grimpe>> getGrimpes({int? seanceId, int? ligneId});
  Future<Grimpe?> getGrimpe(int id);
  Future<Grimpe> createGrimpe(Grimpe grimpe);
  Future<Grimpe> updateGrimpe(Grimpe grimpe);
  Future<void> deleteGrimpe(int id);
}
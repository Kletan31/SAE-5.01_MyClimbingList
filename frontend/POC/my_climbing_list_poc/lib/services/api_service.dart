import 'package:my_climbing_list_poc/models/contest.dart';
import 'package:my_climbing_list_poc/models/ligne.dart';
import 'package:my_climbing_list_poc/models/salle.dart';
import 'package:my_climbing_list_poc/models/suivi.dart';
import 'package:my_climbing_list_poc/models/user.dart';

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
}

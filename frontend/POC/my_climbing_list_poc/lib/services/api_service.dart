import 'package:my_climbing_list_poc/models/contest.dart';
import 'package:my_climbing_list_poc/models/ligne.dart';
import 'package:my_climbing_list_poc/models/salle.dart';

abstract class ApiService {
  Future<List<Salle>> getSalles();
  Future<List<Ligne>> getLignes({int? salleId, int? userId});
  Future<List<Contest>> getContests();
}

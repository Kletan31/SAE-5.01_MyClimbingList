import 'dart:convert';
import 'dart:math';
import 'package:flutter/services.dart';
import 'package:my_climbing_list_poc/models/contest_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/models/suivi_model.dart';
import 'package:my_climbing_list_poc/models/user_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

class MockApiService implements ApiService {
  Map<String, dynamic>? _cache;

  Future<Map<String, dynamic>> _data() async {
    return _cache ??= jsonDecode(
      await rootBundle.loadString('assets/mock/data.json'),
    ) as Map<String, dynamic>;
  }

  // ---------- Helpers génériques, communs à toutes les ressources ----------

  // La liste (modifiable) d'une table : "salles", "lignes", ...
  Future<List<Map<String, dynamic>>> _table(String name) async {
    final d = await _data();
    return (d[name] as List).cast<Map<String, dynamic>>();
  }

  Future<Map<String, dynamic>?> _find(String table, int id) async {
    final rows = await _table(table);
    final i = rows.indexWhere((r) => r['id'] == id);
    return i == -1 ? null : rows[i];
  }

  // Simule le serveur : attribue l'id (plus grand existant + 1)
  Future<Map<String, dynamic>> _insert(
      String table, Map<String, dynamic> json) async {
    final rows = await _table(table);
    final id = rows.fold<int>(0, (m, r) => max(m, r['id'] as int)) + 1;
    final created = {...json, 'id': id};
    rows.add(created);
    return created;
  }

  Future<void> _replace(String table, int id, Map<String, dynamic> json) async {
    final rows = await _table(table);
    final i = rows.indexWhere((r) => r['id'] == id);
    if (i == -1) throw Exception('$table/$id introuvable');
    rows[i] = json;
  }

  Future<void> _remove(String table, int id) async =>
      (await _table(table)).removeWhere((r) => r['id'] == id);

  // ---------- Salles ----------
  @override
  Future<List<Salle>> getSalles() async =>
      (await _table('salles')).map(Salle.fromJson).toList();

  @override
  Future<Salle?> getSalle(int id) async {
    final r = await _find('salles', id);
    return r == null ? null : Salle.fromJson(r);
  }

  @override
  Future<Salle> createSalle(Salle s) async =>
      Salle.fromJson(await _insert('salles', s.toJson()));

  @override
  Future<Salle> updateSalle(Salle s) async {
    await _replace('salles', s.id, s.toJson());
    return s;
  }

  @override
  Future<void> deleteSalle(int id) => _remove('salles', id);

  // ---------- Lignes ----------
  @override
  Future<List<Ligne>> getLignes({int? salleId, int? userId}) async =>
      (await _table('lignes'))
          .map(Ligne.fromJson)
          .where((l) =>
              (salleId == null || l.salleId == salleId) &&
              (userId == null || l.userId == userId))
          .toList();

  @override
  Future<Ligne?> getLigne(int id) async {
    final r = await _find('lignes', id);
    return r == null ? null : Ligne.fromJson(r);
  }

  @override
  Future<Ligne> createLigne(Ligne l) async =>
      Ligne.fromJson(await _insert('lignes', l.toJson()));

  @override
  Future<Ligne> updateLigne(Ligne l) async {
    await _replace('lignes', l.id, l.toJson());
    return l;
  }

  @override
  Future<void> deleteLigne(int id) => _remove('lignes', id);

  @override
  Future<List<Suivi>> getSuivis(int userId) async => (await _table('suivis'))
      .map(Suivi.fromJson)
      .where((s) => s.idUtilisateur == userId)
      .toList();

  @override
  Future<void> addSuivi(Suivi s) async =>
      (await _table('suivis')).add(s.toJson());

  @override
  Future<void> removeSuivi(Suivi s) async =>
      (await _table('suivis')).removeWhere((r) =>
          r['id_utilisateur'] == s.idUtilisateur && r['id_salle'] == s.idSalle);

  // ---------- Users ----------
  @override
  Future<List<User>> getUsers() async =>
      (await _table('users')).map(User.fromJson).toList();

  @override
  Future<User?> getUser(int id) async {
    final r = await _find('users', id);
    return r == null ? null : User.fromJson(r);
  }

  @override
  Future<User> createUser(User u) async =>
      User.fromJson(await _insert('users', u.toJson()));

  @override
  Future<User> updateUser(User u) async {
    await _replace('users', u.id, u.toJson());
    return u;
  }

  @override
  Future<void> deleteUser(int id) => _remove('users', id);

  // ---------- Contests ----------
  @override
  Future<List<Contest>> getContests() async =>
      (await _table('contests')).map(Contest.fromJson).toList();

  @override
  Future<Contest?> getContest(int id) async {
    final r = await _find('contests', id);
    return r == null ? null : Contest.fromJson(r);
  }

  @override
  Future<Contest> createContest(Contest c) async =>
      Contest.fromJson(await _insert('contests', c.toJson()));

  @override
  Future<Contest> updateContest(Contest c) async {
    await _replace('contests', c.id, c.toJson());
    return c;
  }

  @override
  Future<void> deleteContest(int id) => _remove('contests', id);
}

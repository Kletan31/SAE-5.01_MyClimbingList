import 'dart:convert';
import 'dart:math';
import 'package:flutter/services.dart';
import 'package:my_climbing_list_poc/models/contest_model.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/models/seance_model.dart';
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

  Future<Map<String, dynamic>?> _find(String table, int id,
      {String idKey = 'id'}) async {
    final rows = await _table(table);
    final i = rows.indexWhere((r) => r[idKey] == id);
    return i == -1 ? null : rows[i];
  }

  // Simule le serveur : attribue l'id (plus grand existant + 1)
  Future<Map<String, dynamic>> _insert(String table, Map<String, dynamic> json,
      {String idKey = 'id'}) async {
    final rows = await _table(table);
    final id = rows.fold<int>(0, (m, r) => max(m, r[idKey] as int)) + 1;
    final created = {...json, idKey: id};
    rows.add(created);
    return created;
  }

  Future<void> _replace(String table, int id, Map<String, dynamic> json,
      {String idKey = 'id'}) async {
    final rows = await _table(table);
    final i = rows.indexWhere((r) => r[idKey] == id);
    if (i == -1) throw Exception('$table/$id introuvable');
    rows[i] = json;
  }

  Future<void> _remove(String table, int id, {String idKey = 'id'}) async =>
      (await _table(table)).removeWhere((r) => r[idKey] == id);

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
  Future<List<Ligne>> getLignes({int? salleId, int? userId}) async {
    // Lignes grimpées par l'utilisateur : grimpe -> séance -> user
    Set<int>? ligneIds;
    if (userId != null) {
      final seanceIds = (await _table('seance'))
          .where((s) => s['id_user'] == userId)
          .map((s) => s['id_seance'] as int)
          .toSet();
      ligneIds = (await _table('grimpe'))
          .where((g) => seanceIds.contains(g['id_seance']))
          .map((g) => g['id_ligne'] as int)
          .toSet();
    }
    return (await _table('lignes'))
        .map(Ligne.fromJson)
        .where((l) =>
            (salleId == null || l.salleId == salleId) &&
            (ligneIds == null || ligneIds.contains(l.id)))
        .toList();
  }

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

  // ---------- Séances ----------
  @override
  Future<List<Seance>> getSeances({int? userId}) async =>
      (await _table('seance'))
          .map(Seance.fromJson)
          .where((s) => userId == null || s.idUser == userId)
          .toList();

  @override
  Future<Seance?> getSeance(int id) async {
    final r = await _find('seance', id, idKey: 'id_seance');
    return r == null ? null : Seance.fromJson(r);
  }

  @override
  Future<Seance> createSeance(Seance s) async =>
      Seance.fromJson(await _insert('seance', s.toJson(), idKey: 'id_seance'));

  @override
  Future<Seance> updateSeance(Seance s) async {
    await _replace('seance', s.idSeance, s.toJson(), idKey: 'id_seance');
    return s;
  }

  // Suppression en cascade : les grimpes de la séance disparaissent aussi
  @override
  Future<void> deleteSeance(int id) async {
    (await _table('grimpe')).removeWhere((r) => r['id_seance'] == id);
    await _remove('seance', id, idKey: 'id_seance');
  }

  // ---------- Grimpes ----------
  @override
  Future<List<Grimpe>> getGrimpes({int? seanceId, int? ligneId}) async =>
      (await _table('grimpe'))
          .map(Grimpe.fromJson)
          .where((g) =>
              (seanceId == null || g.idSeance == seanceId) &&
              (ligneId == null || g.idLigne == ligneId))
          .toList();

  @override
  Future<Grimpe?> getGrimpe(int id) async {
    final r = await _find('grimpe', id, idKey: 'id_grimpe');
    return r == null ? null : Grimpe.fromJson(r);
  }

  @override
  Future<Grimpe> createGrimpe(Grimpe g) async =>
      Grimpe.fromJson(await _insert('grimpe', g.toJson(), idKey: 'id_grimpe'));

  @override
  Future<Grimpe> updateGrimpe(Grimpe g) async {
    await _replace('grimpe', g.idGrimpe, g.toJson(), idKey: 'id_grimpe');
    return g;
  }

  @override
  Future<void> deleteGrimpe(int id) =>
      _remove('grimpe', id, idKey: 'id_grimpe');
}

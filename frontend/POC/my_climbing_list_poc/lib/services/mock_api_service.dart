import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:my_climbing_list_poc/models/ligne.dart';
import 'package:my_climbing_list_poc/models/salle.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/models/contest.dart';

class MockApiService implements ApiService {
  Map<String, dynamic>? _cache;

  Future<Map<String, dynamic>> _data() async {
    // chargé une seule fois, puis gardé en mémoire
    return _cache ??= jsonDecode(
      await rootBundle.loadString('assets/mock/data.json'),
    ) as Map<String, dynamic>;
  }

  @override
  Future<List<Salle>> getSalles() async {
    final d = await _data();
    return (d['salles'] as List).map((e) => Salle.fromJson(e)).toList();
  }

  @override
  Future<List<Ligne>> getLignes({int? salleId, int? userId}) async {
    final d = await _data();
    return (d['lignes'] as List)
        .map((e) => Ligne.fromJson(e))
        .where((l) =>
            (salleId == null || l.salleId == salleId) &&
            (userId == null || l.userId == userId))
        .toList();
  }

  @override
  Future<List<Contest>> getContests() async {
    final d = await _data();
    return (d['contests'] as List).map((e) => Contest.fromJson(e)).toList();
  }
}

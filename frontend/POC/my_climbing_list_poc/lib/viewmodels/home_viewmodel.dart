import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

// POC : pas d'authentification, on prend l'utilisateur 1
const int _userId = 1;

class HomeViewModel extends ChangeNotifier {
  final ApiService _api;
  HomeViewModel(this._api);

  List<Session> sessions = [];
  bool chargement = false;
  String? erreur;

  Future<void> charger() async {
    chargement = true;
    erreur = null;
    notifyListeners();
    try {
      final salles = await _api.getSalles();
      final noms = {for (final s in salles) s.id: s.nom};
      final lignes = await _api.getLignes(userId: _userId);

      // Une séance = même salle + même jour + même type
      final groupes = <String, List<Ligne>>{};
      for (final l in lignes) {
        final d = l.dateCreation;
        groupes
            .putIfAbsent(
                '${l.salleId}|${d.year}-${d.month}-${d.day}|${l.type}', () => [])
            .add(l);
      }

      sessions = [
        for (final g in groupes.values)
          Session(
              nom: noms[g.first.salleId] ?? 'Salle ${g.first.salleId}',
              lignes: g),
      ]..sort((a, b) => b.date.compareTo(a.date));
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  // ---------- Weekly overview (semaine en cours, depuis lundi) ----------
  List<Session> get sessionsSemaine {
    final now = DateTime.now();
    final lundi = DateTime(now.year, now.month, now.day)
        .subtract(Duration(days: now.weekday - 1));
    return sessions.where((s) => !s.date.isBefore(lundi)).toList();
  }

  int get nbSessionsSemaine => sessionsSemaine.length;
  int get ascentsSemaine =>
      sessionsSemaine.fold(0, (t, s) => t + s.ascents);
  int get topsSemaine => sessionsSemaine.fold(0, (t, s) => t + s.tops);
  String? get maxSemaine =>
      cotationMax(sessionsSemaine.map((s) => s.max).whereType<String>());
}

/// Séance calculée à partir des [Ligne] de l'API.
class Session {
  final String nom;
  final List<Ligne> lignes;
  Session({required this.nom, required this.lignes});

  DateTime get date => lignes.first.dateCreation;
  bool get estBloc => lignes.first.type.toLowerCase().contains('bloc');
  int get ascents => lignes.length;
  // POC : un "top" = ligne dont les propriétés contiennent "top"
  int get tops => lignes.where((l) => l.proprietes.contains('top')).length;
  String? get max => cotationMax(lignes.map((l) => l.cotation));
}

/// "6a" -> 60, "6a+" -> 61, "6b" -> 63 ... inconnu -> -1
int niveauCotation(String cotation) {
  final m = RegExp(r'^(\d)([abc])(\+?)$', caseSensitive: false)
      .firstMatch(cotation.trim());
  if (m == null) return -1;
  return int.parse(m[1]!) * 10 +
      (m[2]!.toLowerCase().codeUnitAt(0) - 97) * 3 +
      (m[3] == '+' ? 1 : 0);
}

String? cotationMax(Iterable<String> cotations) {
  String? max;
  for (final c in cotations) {
    if (max == null || niveauCotation(c) > niveauCotation(max)) max = c;
  }
  return max;
}
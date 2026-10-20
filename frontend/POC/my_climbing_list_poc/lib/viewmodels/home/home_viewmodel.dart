import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/services/api_events.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

// POC : pas d'authentification, on prend l'utilisateur 1
const int _userId = 1;

class HomeViewModel extends ChangeNotifier {
  final ApiService _api;
  late final void Function() _desabonner;
  bool _disposed = false;

  HomeViewModel(this._api, ApiEvents events) {
    // Ce que l'accueil affiche : séances, grimpes, lignes et noms de salles
    _desabonner = events.ecouter(
      {Ressource.seance, Ressource.grimpe, Ressource.lignes, Ressource.salles},
      () => charger(silencieux: true),
    );
  }

  @override
  void dispose() {
    _disposed = true;
    _desabonner(); // sans ça, un écran fermé continuerait d'écouter
    super.dispose();
  }

  List<Session> sessions = [];
  bool chargement = false;
  String? erreur;

  Future<void> charger({bool silencieux = false}) async {
    if (!silencieux) {
      chargement = true;
      erreur = null;
      notifyListeners();
    }
    try {
      final salles = await _api.getSalles();
      final nomsSalles = {for (final s in salles) s.id: s.nom};
      final lignes = {for (final l in await _api.getLignes()) l.id: l};
      final seances = await _api.getSeances(userId: _userId);
      final grimpes = await _api.getGrimpes();

      sessions = [
        for (final s in seances)
          () {
            final items = [
              for (final g in grimpes.where((g) => g.idSeance == s.idSeance))
                if (lignes[g.idLigne] != null)
                  LigneGrimpee(ligne: lignes[g.idLigne]!, grimpe: g),
            ];
            // Une séance peut toucher plusieurs salles (via ses lignes)
            final noms = {
              for (final i in items)
                nomsSalles[i.ligne.salleId] ?? 'Salle ${i.ligne.salleId}'
            };
            return Session(
              id: s.idSeance,
              date: s.date,
              nom: noms.isEmpty ? 'Séance' : noms.join(', '),
              items: items,
            );
          }(),
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
  int get ascentsSemaine => sessionsSemaine.fold(0, (t, s) => t + s.ascents);
  int get topsSemaine => sessionsSemaine.fold(0, (t, s) => t + s.tops);
  String? get maxSemaine =>
      cotationMax(sessionsSemaine.map((s) => s.max).whereType<String>());
}

/// Une ligne grimpée pendant une séance (jointure grimpe + ligne).
class LigneGrimpee {
  final Ligne ligne;
  final Grimpe grimpe;
  LigneGrimpee({required this.ligne, required this.grimpe});
}

/// Séance construite à partir de [Seance], [Grimpe] et [Ligne] de l'API.
class Session {
  final int id;
  final DateTime date;
  final String nom;
  final List<LigneGrimpee> items;
  Session(
      {required this.id,
      required this.date,
      required this.nom,
      required this.items});

  bool get _toutBloc =>
      items.every((i) => i.ligne.type.toLowerCase().contains('bloc'));
  bool get _toutVoie =>
      items.every((i) => !i.ligne.type.toLowerCase().contains('bloc'));
  String get typeLabel => items.isEmpty
      ? '-'
      : (_toutBloc ? 'Boulder' : (_toutVoie ? 'Route' : 'Mixte'));

  /// Ascent = nombre total de montées
  int get ascents => items.fold(0, (t, i) => t + i.grimpe.montee);

  /// Top = nombre de lignes réussies
  int get tops => items.fold(0, (t, i) => t + i.grimpe.top);

  /// Max = cotation la plus haute parmi les lignes réussies
  String? get max => cotationMax(
      items.where((i) => i.grimpe.top > 0).map((i) => i.ligne.cotation));
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

import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/seance_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

/// Brouillon : une ligne sélectionnée et les compteurs saisis (pas encore envoyé à l'API).
class LigneSeance {
  final Ligne ligne;
  int montee = 0;
  int top = 0;
  LigneSeance(this.ligne);
}

class AjoutSeanceViewModel extends ChangeNotifier {
  final ApiService _api;

  AjoutSeanceViewModel(this._api, List<Ligne> lignes)
      : entrees = lignes.map(LigneSeance.new).toList();

  // POC : il n'y a pas encore d'utilisateur connecté
  static const _idUtilisateur = 1;

  final List<LigneSeance> entrees;
  DateTime date = _aujourdhui();
  bool enregistrement = false;
  String? erreur;

  // Date du jour sans l'heure
  static DateTime _aujourdhui() {
    final n = DateTime.now();
    return DateTime(n.year, n.month, n.day);
  }

  // Renvoyé à la page précédente par "Ajouter une ouverture"
  List<Ligne> get lignesSelectionnees => entrees.map((e) => e.ligne).toList();

  void changerDate(DateTime d) {
    date = d;
    notifyListeners();
  }

  // delta vaut +1 ou -1 ; max(0, ...) empêche de descendre sous zéro
  void changerMontee(LigneSeance e, int delta) {
    e.montee = max(0, e.montee + delta);
    notifyListeners();
  }

  void changerTop(LigneSeance e, int delta) {
    e.top = max(0, e.top + delta);
    notifyListeners();
  }

  void retirer(LigneSeance e) {
    entrees.remove(e);
    notifyListeners();
  }

  /// Renvoie true si tout a été enregistré.
  Future<bool> enregistrer() async {
    // Règle choisie : on ne garde que les lignes réellement grimpées
    final aSauver = entrees.where((e) => e.montee > 0 || e.top > 0).toList();
    if (aSauver.isEmpty) {
      erreur = 'Renseigne au moins une montée ou un top.';
      notifyListeners();
      return false;
    }

    enregistrement = true;
    erreur = null;
    notifyListeners();
    try {
      // 1. la séance d'abord : c'est elle qui fournit l'id
      final seance = await _api.createSeance(
        Seance(idSeance: 0, idUser: _idUtilisateur, date: date), // id ignoré
      );
      // 2. puis une grimpe par ligne, rattachée à cette séance
      for (final e in aSauver) {
        await _api.createGrimpe(Grimpe(
          idGrimpe: 0, // ignoré
          idSeance: seance.idSeance,
          idLigne: e.ligne.id,
          montee: e.montee,
          top: e.top,
          flash: false, // POC : pas de flash dans la maquette
        ));
      }
      return true;
    } catch (err) {
      erreur = err.toString();
      return false;
    } finally {
      enregistrement = false;
      notifyListeners();
    }
  }
}
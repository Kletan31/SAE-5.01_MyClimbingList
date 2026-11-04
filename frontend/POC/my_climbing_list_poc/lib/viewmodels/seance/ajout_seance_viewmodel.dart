import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/seance_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

class LigneSeance {
  final Ligne ligne;
  int montee = 0;
  int top = 0;
  bool flash = false;
  LigneSeance(this.ligne);
}

class AjoutSeanceViewModel extends ChangeNotifier {
  final ApiService _api;

  AjoutSeanceViewModel(this._api, List<Ligne> lignes)
      : entrees = lignes.map(LigneSeance.new).toList();

  // POC : id utilisateur codé en dur
  static const _idUtilisateur = 1;

  final List<LigneSeance> entrees;
  DateTime date = _aujourdhui();
  bool enregistrement = false;
  String? erreur;

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

  void changerMontee(LigneSeance e, int delta) {
    int maxValue = e.flash == true ? 1 : 0 ; // mettre au minimum 1 montée si flash
    e.montee = max(maxValue, e.montee + delta);
    if (e.montee < e.top) {
      e.top -= 1;
    }
    notifyListeners();
  }

  void changerTop(LigneSeance e, int delta) {
    e.top = max(0, e.top + delta);
    if (e.top > e.montee) {
      e.montee += 1;
    }
    notifyListeners();
  }

  void retirer(LigneSeance e) {
    entrees.remove(e);
    notifyListeners();
  }

  Future<bool> enregistrer() async {
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
      final seance = await _api.createSeance(
        Seance(idSeance: 0, idUser: _idUtilisateur, date: date), // id ignoré
      );

      for (final e in aSauver) {
        await _api.createGrimpe(Grimpe(
          idGrimpe: 0, // ignoré
          idSeance: seance.idSeance,
          idLigne: e.ligne.id,
          montee: e.montee,
          top: e.top,
          flash: e.flash,
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

  void changerFlash(LigneSeance e) {
    e.flash = !e.flash;
    if (e.top == 0) {
      changerTop(e, 1);
    }
    notifyListeners();
  }
}

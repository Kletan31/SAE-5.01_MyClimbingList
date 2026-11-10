import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/seance_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

const user_id = 1;

class ProjectsViewmodel extends ChangeNotifier {
  final ApiService _api;
  ProjectsViewmodel(this._api);

  List<Seance> seances = [];
  List<Ligne> lignes = [];
  List<Grimpe> grimpes = [];
  bool chargement = false;
  String? erreur;

  Future<void> charger() async {
    chargement = true;
    erreur = null;
    notifyListeners();
    try {
      seances = await _api.getSeances(userId: user_id);
      lignes = await _api.getLignes();

      final seanceIds = seances.map((s) => s.idSeance).toSet();
      final ligneIds = lignes.map((l) => l.id).toSet();
      grimpes = [
        for (final grimpe in await _api.getGrimpes())
          if (seanceIds.contains(grimpe.idSeance) &&
              ligneIds.contains(grimpe.idLigne) &&
              grimpe.top == 0 &&
              grimpe.montee > 0)
            grimpe,
      ];
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  Future<void> supprimer(int id) async {
    await _api.deleteSeance(id);
    grimpes = grimpes.where((g) => g.idSeance != id).toList();
    // if (grimpes.length == 0) {
    //   seances = seances.where((s) => s.idSeance != id).toList();
    // }
    notifyListeners();
  }
}

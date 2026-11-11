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

  DateTime? datePremiereMontee(int idLigne) {
    final dates = _datesMonteesPourLigne(idLigne);
    if (dates.isEmpty) return null;
    return dates.reduce((a, b) => a.isBefore(b) ? a : b);
  }

  DateTime? dateDerniereMontee(int idLigne) {
    final dates = _datesMonteesPourLigne(idLigne);
    if (dates.isEmpty) return null;
    return dates.reduce((a, b) => a.isAfter(b) ? a : b);
  }

  int nombreMontees(int idLigne) => grimpes
      .where((grimpe) => grimpe.idLigne == idLigne)
      .fold(0, (total, grimpe) => total + grimpe.montee);

  List<DateTime> _datesMonteesPourLigne(int idLigne) {
    final seanceParId = {
      for (final seance in seances) seance.idSeance: seance,
    };

    return [
      for (final grimpe in grimpes)
        if (grimpe.idLigne == idLigne &&
            seanceParId.containsKey(grimpe.idSeance))
          seanceParId[grimpe.idSeance]!.date,
    ];
  }
}

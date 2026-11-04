import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

const int _userId = 1;

class CarnetItem {
  final Ligne ligne;
  final Grimpe grimpe;
  final DateTime date;
  final String salle;

  const CarnetItem({
    required this.ligne,
    required this.grimpe,
    required this.date,
    required this.salle,
  });
}

class CarnetViewModel extends ChangeNotifier {
  final ApiService _api;
  CarnetViewModel(this._api);

  bool chargement = true;
  String? erreur;
  bool flashActif = false;
  bool topActif = false;
  List<CarnetItem> _items = [];

  Future<void> charger() async {
    chargement = true;
    erreur = null;
    notifyListeners();
    try {
      final lignes = {
        for (final ligne in await _api.getLignes()) ligne.id: ligne
      };
      final salles = {
        for (final salle in await _api.getSalles()) salle.id: salle.nom
      };
      final seances = await _api.getSeances(userId: _userId);
      final dates = {
        for (final seance in seances) seance.idSeance: seance.date
      };
      _items = [
        for (final grimpe in await _api.getGrimpes())
          if (dates[grimpe.idSeance] != null && lignes[grimpe.idLigne] != null)
            CarnetItem(
              ligne: lignes[grimpe.idLigne]!,
              grimpe: grimpe,
              date: dates[grimpe.idSeance]!,
              salle: salles[lignes[grimpe.idLigne]!.salleId] ??
                  'Salle ${lignes[grimpe.idLigne]!.salleId}',
            ),
      ]..sort((a, b) => b.date.compareTo(a.date));
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  void changerFlash() {
    flashActif = !flashActif;
    notifyListeners();
  }

  void changerTop() {
    topActif = !topActif;
    notifyListeners();
  }

  List<CarnetItem> get items => _items.where((item) {
        return (!flashActif || item.grimpe.flash) &&
            (!topActif || item.grimpe.top > 0);
      }).toList();
}

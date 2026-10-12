import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

class SalleViewModel extends ChangeNotifier {
  final ApiService _api;
  SalleViewModel(this._api);

  List<Salle> salles = [];
  bool chargement = false;
  String? erreur;

  Future<void> charger() async {
    chargement = true;
    erreur = null;
    notifyListeners();
    try {
      salles = await _api.getSalles();
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  Future<void> ajouter(Salle s) async {
    final creee = await _api.createSalle(s);
    salles = [...salles, creee];
    notifyListeners();
  }

  Future<void> modifier(Salle s) async {
    final maj = await _api.updateSalle(s);
    salles = [for (final x in salles) x.id == maj.id ? maj : x];
    notifyListeners();
  }

  Future<void> supprimer(int id) async {
    await _api.deleteSalle(id);
    salles = salles.where((s) => s.id != id).toList();
    notifyListeners();
  }
}

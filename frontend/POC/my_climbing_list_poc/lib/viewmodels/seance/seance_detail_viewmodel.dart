import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

class SeanceDetailViewModel extends ChangeNotifier {
  final ApiService _api;
  final int salleId;
  SeanceDetailViewModel(this._api, this.salleId);

  // --- état de l'écran ---
  bool chargement = true;
  String? erreur;
  Salle? salle; // pour le nom dans le header
  TypeLigne type = TypeLigne.voie; // le double bouton
  bool vueCarte = true; // le bouton carte/liste
  String? secteur; // secteur sélectionné (vue carte)

  List<Ligne> _lignes = [];
  final Set<int> _fait = {}; // ids des lignes cochées

  // --- getters : ce que la vue affiche ---
  // Vue liste : toute la salle, filtrée voie/bloc
  List<Ligne> get lignesFiltrees =>
      _lignes.where((l) => l.type == type.name).toList();

  // Secteurs présents pour le type sélectionné
  List<String> get secteursDisponibles => lignesFiltrees
      .map((l) => l.secteur)
      .whereType<String>() // ignore les null
      .toSet()
      .toList();

  // Vue carte : seulement le secteur sélectionné
  List<Ligne> get lignesDuSecteur =>
      lignesFiltrees.where((l) => l.secteur == secteur).toList();

  bool estFaite(int ligneId) => _fait.contains(ligneId);

  // Les voies et les blocs n'ont pas forcément les mêmes secteurs :
  // on reprend le premier secteur existant pour le type courant
  void _initSecteur() {
    final dispo = secteursDisponibles;
    secteur = dispo.isEmpty ? null : dispo.first;
  }

  // --- actions ---
  Future<void> charger() async {
    try {
      salle = await _api.getSalle(salleId);
      _lignes = await _api.getLignes(salleId: salleId);
      _initSecteur();
      debugPrint('secteurs : $secteursDisponibles | choisi : $secteur');
      debugPrint('secteurs bruts : ${_lignes.map((l) => l.secteur).toList()}');
      // TODO: charger les suivis de l'utilisateur -> remplir _fait
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  void changerType(TypeLigne t) {
    type = t;
    _initSecteur(); // le secteur doit exister pour ce type
    notifyListeners();
  }

  void basculerVue() {
    vueCarte = !vueCarte;
    notifyListeners();
  }

  // Appelée plus tard par la carte 2D au clic sur un secteur
  void choisirSecteur(String s) {
    secteur = s;
    notifyListeners();
  }

  Future<void> basculerFait(int ligneId) async {
    // mise à jour "optimiste" : l'UI réagit tout de suite
    _fait.contains(ligneId) ? _fait.remove(ligneId) : _fait.add(ligneId);
    notifyListeners();
    // puis on persiste (écriture dans data.json côté mock, route Symfony plus tard)
    // await _api.enregistrerSuivi(ligneId, _fait.contains(ligneId));
  }
}

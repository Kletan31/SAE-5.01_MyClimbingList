import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';

class SeanceDetailViewModel extends ChangeNotifier {
  final ApiService _api;
  final int salleId;
  SeanceDetailViewModel(this._api, this.salleId);

  bool chargement = true;
  String? erreur;
  Salle? salle; // pour le nom dans le header
  TypeLigne type = TypeLigne.voie; 
  bool vueCarte = true;
  String? secteur;
  final Set<int> _selection = {}; // id des lignes sélectionnées

  bool estSelectionnee(int ligneId) => _selection.contains(ligneId);
  bool get aSelection => _selection.isNotEmpty; // pilote l'affichage du bouton
  int get nbSelection => _selection.length;

  List<Ligne> _lignes = [];
  final Set<int> _fait = {}; // ids des lignes cochées

  List<Ligne> get lignesSelectionnees =>
      _lignes.where((l) => _selection.contains(l.id)).toList();

  // Vue liste : toute la salle, filtrée voie/bloc
  List<Ligne> get lignesFiltrees =>
      _lignes.where((l) => l.type == type.name).toList();

  // Secteurs présents pour le type sélectionné
  List<String> get secteursDisponibles => lignesFiltrees
      .map((l) => l.secteur)
      .whereType<String>()
      .toSet()
      .toList();

  List<Ligne> get lignesDuSecteur =>
      lignesFiltrees.where((l) => l.secteur == secteur).toList();

  bool estFaite(int ligneId) => _fait.contains(ligneId);

  void _initSecteur() {
    final dispo = secteursDisponibles;
    secteur = dispo.isEmpty ? null : dispo.first;
  }

  Future<void> charger() async {
    try {
      salle = await _api.getSalle(salleId);
      _lignes = await _api.getLignes(salleId: salleId);
      _initSecteur();
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  void changerType(TypeLigne t) {
    type = t;
    _initSecteur();
    notifyListeners();
  }

  void basculerVue() {
    vueCarte = !vueCarte;
    notifyListeners();
  }

  void choisirSecteur(String s) {
    secteur = s;
    notifyListeners();
  }

  Future<void> basculerFait(int ligneId) async {

    _fait.contains(ligneId) ? _fait.remove(ligneId) : _fait.add(ligneId);
    notifyListeners();
    // await _api.enregistrerSuivi(ligneId, _fait.contains(ligneId));
  }

  void basculerSelection(int ligneId) {
    if (!_selection.remove(ligneId)) _selection.add(ligneId);
    notifyListeners(); // redessine l'écran
  }

  void viderSelection() {
    _selection.clear();
    notifyListeners();
  }
}

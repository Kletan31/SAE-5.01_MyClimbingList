import 'package:flutter/foundation.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/models/user_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/home/home_viewmodel.dart';

// POC : pas d'authentification, on prend l'utilisateur 1
// TODO(auth): même constante que dans home_viewmodel.dart. À remplacer par
// l'id de l'utilisateur connecté (voir le TODO(auth) de home_viewmodel.dart),
// puis supprimer cette constante.
const int _userId = 1;

/// Nombre de tops et de flashs sur un ensemble de lignes grimpées.
class StatsGrimpe {
  final int top, flash;
  const StatsGrimpe({this.top = 0, this.flash = 0});
}

class AccountViewModel extends ChangeNotifier {
  final ApiService _api;
  AccountViewModel(this._api);

  // --- état de l'écran ---
  bool chargement = true;
  String? erreur;
  User? user;
  TypeLigne type = TypeLigne.voie; // le double bouton Route / Bloc
  int nbSeances = 0;

  List<LigneGrimpee> _items = [];
  Map<int, String> _nomsSalles = {};

  // --- actions ---
  Future<void> charger() async {
    chargement = true;
    erreur = null;
    notifyListeners();
    try {
      user = await _api.getUser(_userId);
      final salles = await _api.getSalles();
      _nomsSalles = {for (final s in salles) s.id: s.nom};
      final lignes = {for (final l in await _api.getLignes()) l.id: l};
      final seances = await _api.getSeances(userId: _userId);
      nbSeances = seances.length;
      final ids = {for (final s in seances) s.idSeance};
      // TODO(perf): filtrer côté API (getGrimpes(userId: ...)) au lieu de
      // charger toutes les grimpes puis filtrer ici.
      _items = [
        for (final g in await _api.getGrimpes())
          if (ids.contains(g.idSeance) && lignes[g.idLigne] != null)
            LigneGrimpee(ligne: lignes[g.idLigne]!, grimpe: g),
      ];
    } catch (e) {
      erreur = e.toString();
    }
    chargement = false;
    notifyListeners();
  }

  void changerType(TypeLigne t) {
    type = t;
    notifyListeners();
  }

  // --- données affichées (pour le type sélectionné) ---
  String get nomUtilisateur => user?.nomUtilisateur ?? '-';

  List<LigneGrimpee> get _itemsType =>
      _items.where((i) => i.ligne.type == type.name).toList();

  StatsGrimpe _stats(Iterable<LigneGrimpee> items) => StatsGrimpe(
        top: items.fold(0, (t, i) => t + i.grimpe.top),
        flash: items.where((i) => i.grimpe.flash).length,
      );

  // TODO : la maquette sépare moulinette et tete, mais l'API ne dit pas
  // comment une voie a été grimpée. Il faut ajouter un champ (ex. "mode" :
  // moulinette / tete) sur `grimpe`, dans data.json, Grimpe et le backend.
  // En attendant : tout est compté en tete, moulinette reste à 0.
  StatsGrimpe get moulinette => const StatsGrimpe();
  StatsGrimpe get tete => _stats(_itemsType);

  /// Stats affichées en mode Bloc (pas de distinction moulinette / tete)
  StatsGrimpe get bloc => _stats(_itemsType);

  /// Salle où l'utilisateur a grimpé le plus de lignes de ce type
  String? get salleFavorite {
    final nb = <int, int>{};
    for (final i in _itemsType) {
      nb[i.ligne.salleId] = (nb[i.ligne.salleId] ?? 0) + 1;
    }
    if (nb.isEmpty) return null;
    final id = nb.entries.reduce((a, b) => b.value > a.value ? b : a).key;
    return _nomsSalles[id] ?? 'Salle $id';
  }

  // TODO(data): `proprietes` mélange profil (inclinaison du mur) et style de
  // grimpe dans la même liste. On les sépare ici avec des listes en dur ;
  // à terme, deux champs distincts côté API (profil / style).
  static const _profils = {'dalle', 'vertical', 'dévers'};
  String? get profilFavori =>
      _proprieteFavorite((p) => _profils.contains(_cle(p)));
  String? get styleFavori =>
      _proprieteFavorite((p) => !_profils.contains(_cle(p)));

  /// Cotation la plus haute parmi les lignes réussies (top)
  String? get cotationMaxi => cotationMax(
      _itemsType.where((i) => i.grimpe.top > 0).map((i) => i.ligne.cotation));

  // "réglette" et "réglettes" sont comptés ensemble
  String _cle(String p) {
    final s = p.trim().toLowerCase();
    return s.endsWith('s') ? s.substring(0, s.length - 1) : s;
  }

  String? _proprieteFavorite(bool Function(String) garder) {
    final nb = <String, int>{};
    final libelle = <String, String>{};
    for (final i in _itemsType) {
      for (final p in i.ligne.proprietes.where(garder)) {
        final k = _cle(p);
        nb[k] = (nb[k] ?? 0) + 1;
        libelle.putIfAbsent(k, () => p);
      }
    }
    if (nb.isEmpty) return null;
    return libelle[nb.entries.reduce((a, b) => b.value > a.value ? b : a).key];
  }
}
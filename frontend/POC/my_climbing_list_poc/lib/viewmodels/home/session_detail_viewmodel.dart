import 'package:flutter/foundation.dart';
import 'package:intl/intl.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/viewmodels/home/home_viewmodel.dart';

/// Cotations affichées dans l'histogramme : 5a, 5b, 5c, 6a ... 9c
final List<String> cotationsHistogramme = [
  for (final n in const [5, 6, 7, 8, 9])
    for (final l in const ['a', 'b', 'c']) '$n$l'
];

/// Logique de l'écran "Détails d'une séance".
/// La séance vient de [HomeViewModel] ; ici on ne fait que la présenter.
class SessionDetailViewModel extends ChangeNotifier {
  final Session session;
  SessionDetailViewModel(this.session);

  String get titre => 'Détails';
  String get nom => session.nom;
  String get date => DateFormat('dd MMM yyyy').format(session.date);
  List<Ligne> get lignes => session.lignes;

  /// Nombre de lignes par cotation ("6a+" est compté dans "6a")
  late final Map<String, int> comptes = _calculerComptes();

  Map<String, int> _calculerComptes() {
    final m = {for (final c in cotationsHistogramme) c: 0};
    for (final l in session.lignes) {
      final c = _normaliser(l.cotation);
      if (m.containsKey(c)) m[c] = m[c]! + 1;
    }
    return m;
  }

  /// Valeur max de l'axe Y (minimum 5 pour garder une échelle lisible)
  int get yMax => comptes.values.fold(5, (a, b) => b > a ? b : a);

  /// Hauteur relative (0..1) de la barre d'une cotation
  double hauteurBarre(String cotation) => (comptes[cotation] ?? 0) / yMax;

  String libelleCotation(Ligne l) => l.cotation.toLowerCase();
  String libelleRelais(Ligne l) => 'Relais: ${l.relais ?? '-'}';
  String libelleProprietes(Ligne l) => l.proprietes.join(', ');

  static String _normaliser(String c) => c.toLowerCase().replaceAll('+', '');
}
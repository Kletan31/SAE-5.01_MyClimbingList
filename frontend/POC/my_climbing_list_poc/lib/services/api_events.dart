import 'dart:async';

/// Ressources de l'API qui peuvent changer (mêmes noms que les tables du mock).
enum Ressource { salles, lignes, users, suivis, contests, seance, grimpe }

class ApiEvents {
  // broadcast : plusieurs viewmodels peuvent écouter en même temps
  final _controller = StreamController<Ressource>.broadcast();

  Stream<Ressource> get changes => _controller.stream;

  /// Appelé par l'API après chaque écriture réussie.
  void notifier(Ressource r) => _controller.add(r);

  /// Appelle [rappel] quand l'une des [ressources] change.
  /// Renvoie la fonction à appeler pour se désabonner.
  void Function() ecouter(Set<Ressource> ressources, void Function() rappel) {
    Timer? attente;
    final abonnement = changes.where(ressources.contains).listen((_) {
      // Regroupe les rafales : 1 séance + N grimpes = 1 seul rechargement
      attente?.cancel();
      attente = Timer(const Duration(milliseconds: 100), rappel);
    });
    return () {
      attente?.cancel();
      abonnement.cancel();
    };
  }

  void dispose() => _controller.close();
}
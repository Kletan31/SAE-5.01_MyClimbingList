import 'dart:async';

enum Ressource { salles, lignes, users, suivis, contests, seance, grimpe }

class ApiEvents {
  // broadcast : plusieurs viewmodels peuvent écouter en même temps
  final _controller = StreamController<Ressource>.broadcast();

  Stream<Ressource> get changes => _controller.stream;

  void notifier(Ressource r) => _controller.add(r);

  // renvoie la fonction à appeler pour se désabonner
  void Function() ecouter(Set<Ressource> ressources, void Function() rappel) {
    Timer? attente;
    final abonnement = changes.where(ressources.contains).listen((_) {
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

class Suivi {
  final int idUtilisateur;
  final int? idSalle;

  Suivi({required this.idUtilisateur, this.idSalle});

  factory Suivi.fromJson(Map<String, dynamic> j) => Suivi(
        idUtilisateur: j['id_utilisateur'],
        idSalle: j['id_salle'],
      );
}
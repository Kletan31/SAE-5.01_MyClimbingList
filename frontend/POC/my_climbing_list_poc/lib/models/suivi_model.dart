class Suivi {
  final int idUtilisateur;
  final int? idSalle;

  Suivi({required this.idUtilisateur, this.idSalle});

  factory Suivi.fromJson(Map<String, dynamic> j) => Suivi(
        idUtilisateur: j['id_utilisateur'],
        idSalle: j['id_salle'],
      );

  Map<String, dynamic> toJson() =>
      {'id_utilisateur': idUtilisateur, 'id_salle': idSalle};
}

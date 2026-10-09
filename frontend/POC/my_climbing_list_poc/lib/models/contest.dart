class Contest {
  final int id;
  final String nom, statut;
  final List<int> idSalles;
  final DateTime dateDebut, dateFin;

  Contest({required this.id, required this.nom, required this.statut, required this.idSalles, required this.dateDebut, required this.dateFin});

  factory Contest.fromJson(Map<String, dynamic> j) => Contest(
        id: j['id'],
        nom: j['nom'],
        statut: j['statut'],
        idSalles: List<int>.from(j['id_salles']),
        dateDebut: DateTime.parse(j['date_debut']),
        dateFin: DateTime.parse(j['date_fin']),
      );
}
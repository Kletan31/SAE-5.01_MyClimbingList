class Seance {
  final int idSeance, idUser;
  final DateTime date;

  Seance(
      {required this.idSeance,
      required this.idUser,
      required this.date});

  factory Seance.fromJson(Map<String, dynamic> j) => Seance(
        idSeance: j['id_seance'],
        idUser: j['id_user'],
        date: DateTime.parse(j['date']),
      );

  Map<String, dynamic> toJson() => {
        'id_seance': idSeance,
        'id_user': idUser,
        'date': date.toIso8601String().split('T').first,
      };
}
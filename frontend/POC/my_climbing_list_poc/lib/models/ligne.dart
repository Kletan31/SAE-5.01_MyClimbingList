class Ligne {
  final int id, userId, salleId;
  final int? relais;
  final String type, cotation, couleur, secteur;
  final List<String> proprietes;
  final DateTime dateCreation;

  Ligne({required this.id, required this.userId, required this.salleId, this.relais, required this.type, required this.cotation, required this.couleur, required this.secteur, required this.proprietes, required this.dateCreation});

  factory Ligne.fromJson(Map<String, dynamic> j) => Ligne(
        id: j['id'],
        userId: j['user_id'],
        salleId: j['salle_id'],
        relais: j['relais'],
        type: j['type'],
        cotation: j['cotation'],
        couleur: j['couleur'],
        secteur: j['secteur'],
        proprietes: List<String>.from(j['proprietes']),
        dateCreation: DateTime.parse(j['date_creation']),
      );
}
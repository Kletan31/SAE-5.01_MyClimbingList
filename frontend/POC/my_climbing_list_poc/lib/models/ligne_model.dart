enum TypeLigne { voie, bloc }

class Ligne {
  final int id, salleId;
  final int? relais;
  final String? secteur;
  final String type, cotation, couleur;
  final List<String> proprietes;
  final DateTime dateCreation;

  Ligne(
      {required this.id,
      required this.salleId,
      this.relais,
      required this.type,
      required this.cotation,
      required this.couleur,
      required this.secteur,
      required this.proprietes,
      required this.dateCreation});

  factory Ligne.fromJson(Map<String, dynamic> j) => Ligne(
        id: j['id'],
        salleId: j['salle_id'],
        relais: j['relais'],
        type: j['type'],
        cotation: j['cotation'],
        couleur: j['couleur'],
        secteur: j['secteur'],
        proprietes: List<String>.from(j['proprietes']),
        dateCreation: DateTime.parse(j['date_creation']),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'salle_id': salleId,
        'relais': relais,
        'type': type,
        'cotation': cotation,
        'couleur': couleur,
        'secteur': secteur,
        'proprietes': proprietes,
        'date_creation': dateCreation.toIso8601String().split('T').first,
      };
}

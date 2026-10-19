class Grimpe {
  final int idGrimpe, idSeance, idLigne, montee, top;
  final bool flash;

  Grimpe(
      {required this.idGrimpe,
      required this.idSeance,
      required this.idLigne,
      required this.montee,
      required this.top,
      required this.flash});

  factory Grimpe.fromJson(Map<String, dynamic> j) => Grimpe(
        idGrimpe: j['id_grimpe'],
        idSeance: j['id_seance'],
        idLigne: j['id_ligne'],
        montee: j['montee'],
        top: j['top'],
        flash: j['flash'],
      );

  Map<String, dynamic> toJson() => {
        'id_grimpe': idGrimpe,
        'id_seance': idSeance,
        'id_ligne': idLigne,
        'montee': montee,
        'top': top,
        'flash': flash,
      };
}
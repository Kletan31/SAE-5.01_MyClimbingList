class Salle {
  final int id;
  final String nom, image, localisation;

  Salle({required this.id, required this.nom, required this.image, required this.localisation});

  factory Salle.fromJson(Map<String, dynamic> j) => Salle(
        id: j['id'],
        nom: j['nom'],
        image: j['image'],
        localisation: j['localisation'],
      );
}
class User {
  final int id;
  final String nom, prenom, nomUtilisateur, motDePasse, mail, genre;
  final DateTime dateInscription;

  User({required this.id, required this.nom, required this.prenom, required this.nomUtilisateur, required this.motDePasse, required this.mail, required this.genre, required this.dateInscription});

  factory User.fromJson(Map<String, dynamic> j) => User(
        id: j['id'],
        nom: j['nom'],
        prenom: j['prenom'],
        nomUtilisateur: j['nom_utilisateur'],
        motDePasse: j['mot_de_passe'],
        mail: j['mail'],
        genre: j['genre'],
        dateInscription: DateTime.parse(j['date_inscription']),
      );
}
import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';

class AjoutSeanceScreen extends StatelessWidget {
  final List<Ligne> lignes;
  const AjoutSeanceScreen({super.key, required this.lignes});

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: const AppHeader(title: 'Ajouter ma séance'),
        body: ListView(children: [
          for (final l in lignes)
            ListTile(
              title: Text('${l.cotation} - ${l.couleur}'),
              subtitle: Text(l.type), // "voie" ou "bloc"
            ),
        ]),
      );
}

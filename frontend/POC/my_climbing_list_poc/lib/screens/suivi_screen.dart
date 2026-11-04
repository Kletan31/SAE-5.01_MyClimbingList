import 'package:flutter/material.dart';
import '../widgets/poc_card.dart';
import '../widgets/app_header.dart';

class SuiviScreen extends StatelessWidget {
  const SuiviScreen({super.key});
  @override
  Widget build(BuildContext c) => Scaffold(
        appBar: const AppHeader(title: 'Suivi'),
        body: SafeArea(
          child: ListView(padding: const EdgeInsets.all(20), children: [
        const SizedBox(height: 20),
        const PocCard(
            title: 'Salle',
            subtitle: 'POC en devemopement de la page suivi',
            icon: Icons.person_outline)
          ]),
        ),
      );
}

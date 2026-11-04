import 'package:flutter/material.dart';
import '../widgets/poc_card.dart';
import '../widgets/app_header.dart';

class RetourScreen extends StatelessWidget {
  const RetourScreen({super.key});
  @override
  Widget build(BuildContext c) => Scaffold(
        appBar: const AppHeader(title: 'Retour'),
        body: SafeArea(
          child: ListView(padding: const EdgeInsets.all(20), children: [
        const SizedBox(height: 20),
        const PocCard(
            title: 'Retour',
            subtitle: 'POC en devemopement de la page retour',
            icon: Icons.person_outline)
          ]),
        ),
      );
}

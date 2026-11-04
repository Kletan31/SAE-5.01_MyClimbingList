import 'package:flutter/material.dart';
import '../widgets/poc_card.dart';
import '../widgets/app_header.dart';

class CarnetScreen extends StatelessWidget {
  final bool showHeader;

  const CarnetScreen({super.key, this.showHeader = true});

  @override
  Widget build(BuildContext c) {
    final body = SafeArea(
          child: ListView(padding: const EdgeInsets.all(20), children: [
        const SizedBox(height: 20),
        const PocCard(
            title: 'Carnet',
            subtitle: 'POC en developement de la page carnet',
            icon: Icons.person_outline),
        const SizedBox(height: 12)
      ]));

    return showHeader
        ? Scaffold(appBar: const AppHeader(title: 'Carnet'), body: body)
        : body;
  }
}

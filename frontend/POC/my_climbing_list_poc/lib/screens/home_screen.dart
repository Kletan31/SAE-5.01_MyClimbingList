import 'package:flutter/material.dart';
import '../widgets/poc_card.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) => SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
    Text('My Climbing List', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
    const SizedBox(height: 6),
    Text('POC — écran d’accueil', style: Theme.of(context).textTheme.bodyLarge),
    const SizedBox(height: 24),
    const PocCard(title: 'Cette semaine', subtitle: 'Aperçu des séances', icon: Icons.calendar_today_outlined),
    const SizedBox(height: 12),
    const PocCard(title: 'Progression', subtitle: 'Niveau / Elo', icon: Icons.trending_up),
    const SizedBox(height: 12),
    const PocCard(title: 'Dernières réalisations', subtitle: 'Historique', icon: Icons.check_circle_outline),
  ]));
}

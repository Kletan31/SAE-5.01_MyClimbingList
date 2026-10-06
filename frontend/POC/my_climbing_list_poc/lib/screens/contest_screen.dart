import 'package:flutter/material.dart';

class ContestScreen extends StatelessWidget {
  const ContestScreen({super.key});
  @override
  Widget build(BuildContext context) => SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
    Text('Topo', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
    const SizedBox(height: 16),
    DropdownButtonFormField<String>(initialValue: 'Salle', decoration: const InputDecoration(labelText: 'Salle', border: OutlineInputBorder()), items: const [DropdownMenuItem(value: 'Salle', child: Text('Salle'))], onChanged: (_) {}),
    const SizedBox(height: 16),
    SegmentedButton<String>(segments: const [ButtonSegment(value: 'Voies', label: Text('Voies')), ButtonSegment(value: 'Bloc', label: Text('Bloc'))], selected: const {'Voies'}, onSelectionChanged: (_) {}),
    const SizedBox(height: 24),
    const _RoutePlaceholder(), const SizedBox(height: 10), const _RoutePlaceholder(), const SizedBox(height: 10), const _RoutePlaceholder(),
  ]));
}
class _RoutePlaceholder extends StatelessWidget { const _RoutePlaceholder(); @override Widget build(BuildContext c) => Card(child: ListTile(leading: const CircleAvatar(child: Icon(Icons.route)), title: const Text('Ouverture'), subtitle: const Text('Prototype — cotation / statut'), trailing: IconButton(onPressed: () {}, icon: const Icon(Icons.check_circle_outline)))); }

import 'package:flutter/material.dart';

class SeanceScreen extends StatelessWidget {
  const SeanceScreen({super.key});
  @override
  Widget build(BuildContext context) => SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
    Text('Nouvelle séance', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
    const SizedBox(height: 20),
    const TextField(decoration: InputDecoration(labelText: 'Salle', border: OutlineInputBorder())),
    const SizedBox(height: 14),
    const TextField(decoration: InputDecoration(labelText: 'Date', border: OutlineInputBorder())),
    const SizedBox(height: 20),
    const Text('Ouvertures sélectionnées', style: TextStyle(fontWeight: FontWeight.bold)),
    const SizedBox(height: 10),
    ...List.generate(3, (i) => CheckboxListTile(value: false, onChanged: (_) {}, title: Text('Ouverture ${i + 1}'), subtitle: const Text('Prototype'))),
    const SizedBox(height: 12),
    FilledButton(onPressed: () {}, child: const Text('Enregistrer')),
  ]));
}

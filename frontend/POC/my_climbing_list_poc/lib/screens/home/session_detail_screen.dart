import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../viewmodels/home_viewmodel.dart';

final _cotations = [
  for (final n in const [5, 6, 7, 8, 9])
    for (final l in const ['a', 'b', 'c']) '$n$l'
];

class SessionDetailScreen extends StatelessWidget {
  final Session session;
  const SessionDetailScreen({super.key, required this.session});

  // Nombre de lignes par cotation ("6a+" est compté dans "6a")
  Map<String, int> get _counts {
    final m = {for (final c in _cotations) c: 0};
    for (final l in session.lignes) {
      final c = l.cotation.toLowerCase().replaceAll('+', '');
      if (m.containsKey(c)) m[c] = m[c]! + 1;
    }
    return m;
  }

  @override
  Widget build(BuildContext context) {
    final counts = _counts;
    final yMax = counts.values.fold(5, (a, b) => b > a ? b : a);

    return Scaffold(
      appBar: AppBar(title: const Text('Détails')),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Column(children: [
            Text(session.nom,
                style: const TextStyle(
                    fontSize: 12, fontWeight: FontWeight.w700)),
            Text(DateFormat('dd MMM yyyy').format(session.date),
                style: const TextStyle(
                    fontSize: 10, fontStyle: FontStyle.italic)),
          ]),
        ),
        SizedBox(
          height: 220,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
              for (final c in _cotations)
                Expanded(
                  child: Column(mainAxisAlignment: MainAxisAlignment.end, children: [
                    Expanded(
                      child: Align(
                        alignment: Alignment.bottomCenter,
                        child: FractionallySizedBox(
                          heightFactor: counts[c]! / yMax,
                          child: Container(
                              width: 8, color: Colors.lightGreen),
                        ),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(c,
                        style: const TextStyle(
                            fontSize: 8, fontWeight: FontWeight.w700)),
                  ]),
                ),
            ]),
          ),
        ),
        const Divider(thickness: 1),
        Expanded(
          child: ListView.separated(
            itemCount: session.lignes.length,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (_, i) {
              final l = session.lignes[i];
              return ListTile(
                title: Text('Relais: ${l.relais ?? '-'}',
                    style: const TextStyle(
                        fontSize: 12, fontStyle: FontStyle.italic)),
                subtitle: Text(l.proprietes.join(', ')),
                trailing: Container(
                  width: 40,
                  height: 40,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.lightBlue, width: 2),
                  ),
                  child: Text(l.cotation.toLowerCase(),
                      style: const TextStyle(fontWeight: FontWeight.w700)),
                ),
              );
            },
          ),
        ),
      ]),
    );
  }
}
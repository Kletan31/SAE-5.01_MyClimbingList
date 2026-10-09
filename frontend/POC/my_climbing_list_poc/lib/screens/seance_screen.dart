import 'package:flutter/material.dart';
import '../models/salle.dart';
import '../services/api_service.dart';
import '../services/mock_api_service.dart';

class SeanceScreen extends StatefulWidget {
  const SeanceScreen({super.key});
  @override
  State<SeanceScreen> createState() => _SeanceScreenState();
}

class _SeanceScreenState extends State<SeanceScreen> {
  // POC : instancié en dur ici, à terme injecté via le viewmodel
  final ApiService _api = MockApiService();
  late final Future<List<Salle>> _salles = _api.getSalles();

  @override
  Widget build(BuildContext context) => SafeArea(
        child: FutureBuilder<List<Salle>>(
          future: _salles,
          builder: (context, snap) {
            if (snap.hasError) return Center(child: Text('Erreur : ${snap.error}'));
            if (!snap.hasData) return const Center(child: CircularProgressIndicator());
            final salles = snap.data!;
            return ListView.separated(
              itemCount: salles.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (_, i) => _SalleCard(salle: salles[i]),
            );
          },
        ),
      );
}

class _SalleCard extends StatelessWidget {
  final Salle salle;
  const _SalleCard({required this.salle});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.all(16),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Image : vient de l'API
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              salle.image,
              width: 110,
              height: 110,
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => Container(
                width: 110,
                height: 110,
                color: Colors.grey.shade300,
                child: const Icon(Icons.image_not_supported),
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                // Nom : vient de l'API
                Flexible(
                  child: Text(salle.nom,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context)
                          .textTheme
                          .titleMedium
                          ?.copyWith(fontWeight: FontWeight.w600)),
                ),
                const SizedBox(width: 8),
                // POC : favori non branché
                const Icon(Icons.star_border, size: 22),
              ]),
              const SizedBox(height: 8),
              // POC : progressions en dur
              const _Progression(label: 'Voie', valeur: 0),
              const SizedBox(height: 10),
              const _Progression(label: 'Bloc', valeur: 0),
            ]),
          ),
          const SizedBox(width: 8),
          // POC : bouton stats non branché
          const Icon(Icons.bar_chart, size: 28),
        ]),
      );
}

// POC : widget temporaire, les % viendront des vraies données (suivi des lignes)
class _Progression extends StatelessWidget {
  final String label;
  final double valeur; // entre 0 et 1
  const _Progression({required this.label, required this.valeur});

  @override
  Widget build(BuildContext context) =>
      Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('$label : ${(valeur * 100).round()}%',
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: LinearProgressIndicator(
            value: valeur,
            minHeight: 12,
            backgroundColor: Colors.grey.shade200,
          ),
        ),
      ]);
}
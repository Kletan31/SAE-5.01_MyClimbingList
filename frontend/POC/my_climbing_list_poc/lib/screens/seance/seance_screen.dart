import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/salle_model.dart';
import '../../services/api_service.dart';
import '../../viewmodels/seance/seance_viewmodel.dart';

class SeanceScreen extends StatelessWidget {
  const SeanceScreen({super.key});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        // context.read<ApiService>() récupère celui déclaré dans main.dart
        create: (context) =>
            SalleViewModel(context.read<ApiService>())..charger(),
        child: const _SeanceView(),
      );
}

class _SeanceView extends StatelessWidget {
  const _SeanceView();

  @override
  Widget build(BuildContext context) {
    // watch : l'écran se redessine à chaque notifyListeners() du viewmodel
    final vm = context.watch<SalleViewModel>();

    return SafeArea(
      child: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : ListView.separated(
                  itemCount: vm.salles.length,
                  separatorBuilder: (_, __) => const Divider(height: 1),
                  itemBuilder: (_, i) => _SalleCard(salle: vm.salles[i]),
                ),
    );
  }
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
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
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

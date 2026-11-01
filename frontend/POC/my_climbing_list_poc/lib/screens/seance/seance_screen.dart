import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/salle_model.dart';
import '../../services/api_service.dart';
import '../../viewmodels/seance/seance_viewmodel.dart';
import '../../widgets/salle_image.dart';
import 'seance_detail_screen.dart';

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
    // l'écran se redessine à chaque notifyListeners() du viewmodel
    final vm = context.watch<SalleViewModel>();

    return SafeArea(
      child: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : ListView.separated(
                  itemCount: vm.salles.length,
                  separatorBuilder: (_, __) => const Divider(height: 20),
                  itemBuilder: (_, i) => _SalleCard(salle: vm.salles[i]),
                ),
    );
  }
}

class _SalleCard extends StatelessWidget {
  const _SalleCard({required this.salle});

  final Salle salle;

  static const double _padding = 5;
  static const double _espacement = 12;

  // paramètres de taille d'image
  static const double _imageFraction = 0.40;
  static const double _imageLargeurMin = 145;
  static const double _imageLargeurMax = 200;

  @override
  Widget build(BuildContext context) => InkWell(
        onTap: () => Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => SeanceDetailScreen(salleId: salle.id),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(_padding),
          child: LayoutBuilder(
            builder: (context, constraints) {
              final imageLargeur = (constraints.maxWidth * _imageFraction)
                  .clamp(_imageLargeurMin, _imageLargeurMax)
                  .toDouble();

              // la hauteur de la carte est celle du texte, l'image s'étire à cette hauteur
              return IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    SalleImage(reference: salle.image, width: imageLargeur),
                    const SizedBox(width: _espacement),
                    Expanded(child: _Infos(salle: salle)),
                  ],
                ),
              );
            },
          ),
        ),
      );
}

// Colonne de texte d'une carte : titre, favori, stats et progressions.
class _Infos extends StatelessWidget {
  const _Infos({required this.salle});

  final Salle salle;

  @override
  Widget build(BuildContext context) {
    final vm = context.read<SalleViewModel>();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      spacing: 2,
      children: [
        Row(
          children: [
            Expanded(
              child: Row(
                children: [
                  Flexible(
                    child: Text(
                      salle.nom,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context)
                          .textTheme
                          .titleMedium
                          ?.copyWith(fontWeight: FontWeight.w600),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // POC : favori appelle une méthode vide
                  _IconeCompacte(
                    icone: Icons.star_border,
                    taille: 22,
                    onPressed: () => vm.mettreFavori(salle.id),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            _IconeCompacte(
              icone: Icons.bar_chart,
              taille: 24,
              onPressed: () => vm.afficherStats(salle.id),
            ),
          ],
        ),
        const SizedBox(height: 8),
        // POC : progressions en dur
        const _Progression(label: 'Voie', valeur: 0),
        const SizedBox(height: 10),
        const _Progression(label: 'Bloc', valeur: 0),
      ],
    );
  }
}

class _IconeCompacte extends StatelessWidget {
  const _IconeCompacte({
    required this.icone,
    required this.taille,
    required this.onPressed,
  });

  final IconData icone;
  final double taille;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) => IconButton(
        onPressed: onPressed,
        padding: EdgeInsets.zero,
        constraints: const BoxConstraints(),
        style: IconButton.styleFrom(
          tapTargetSize: MaterialTapTargetSize.shrinkWrap,
        ),
        icon: Icon(icone, size: taille),
      );
}

// POC : widget temporaire, les % viendront des vraies données
// à refaire une fois l'API intégrée
class _Progression extends StatelessWidget {
  const _Progression({required this.label, required this.valeur});

  final String label;
  final double valeur; // entre 0 et 1

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

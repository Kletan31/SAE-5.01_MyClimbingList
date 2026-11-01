import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/screens/seance/ajout_seance_screen.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/seance/seance_detail_viewmodel.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';
import 'package:my_climbing_list_poc/widgets/ligne_table.dart';
import 'package:provider/provider.dart';

class SeanceDetailScreen extends StatelessWidget {
  final int salleId;
  const SeanceDetailScreen({super.key, required this.salleId});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (context) =>
            SeanceDetailViewModel(context.read<ApiService>(), salleId)
              ..charger(),
        child: const _SeanceDetailView(),
      );
}

class _SeanceDetailView extends StatelessWidget {
  const _SeanceDetailView();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SeanceDetailViewModel>();

    final title = vm.chargement
        ? 'Chargement...'
        : vm.erreur != null
            ? 'Erreur'
            : vm.salle?.nom ?? 'Salle inconnue';

    return Scaffold(
      appBar: AppHeader(title: title),
      body: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : vm.salle == null
                  ? const Center(child: Text('Salle introuvable'))
                  : Column(children: [
                      const _BandeauSuperieur(),
                      Expanded(
                        // carte mock ou liste selon le bouton du bandeau
                        child:
                            vm.vueCarte ? const _VueCarte() : const _VueListe(),
                      ),
                    ]),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: vm.aSelection // null = pas de bouton
          ? FloatingActionButton.extended(
              heroTag: null, // évite un conflit d'animation entre pages
              icon: const Icon(Icons.add),
              label: Text('Ajouter ma séance (${vm.nbSelection})'),
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) =>
                      AjoutSeanceScreen(lignes: vm.lignesSelectionnees),
                ),
              ),
            )
          : null,
    );
  }
}

class _BandeauSuperieur extends StatelessWidget {
  const _BandeauSuperieur();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SeanceDetailViewModel>();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
      child: Row(children: [
        const SizedBox(width: 48),
        Expanded(
          child: Center(
            child: SegmentedButton<TypeLigne>(
              showSelectedIcon: false,
              segments: const [
                ButtonSegment(value: TypeLigne.voie, label: Text('Voie')),
                ButtonSegment(value: TypeLigne.bloc, label: Text('Bloc')),
              ],
              selected: {vm.type},
              onSelectionChanged: (s) => vm.changerType(s.first),
            ),
          ),
        ),
        IconButton(
          onPressed: vm.basculerVue,
          icon: Icon(vm.vueCarte ? Icons.list : Icons.map_outlined),
        ),
      ]),
    );
  }
}

class _VueCarte extends StatelessWidget {
  const _VueCarte();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SeanceDetailViewModel>();

    return Column(children: [
      // TODO: remplacer par la carte 2D interactive
      Expanded(
        flex: 3,
        child: Container(
          color: Colors.grey.shade200,
          child: const Center(child: Text('Carte 2D (à venir)')),
        ),
      ),
      Expanded(
        flex: 2,
        child: LigneTable(
          lignes: vm.lignesDuSecteur,
          afficherRelais: false,
          estFaite: vm.estFaite,
          onToggle: vm.basculerFait,
          estSelectionnee: vm.estSelectionnee,
          onSelect: vm.basculerSelection,
        ),
      ),
    ]);
  }
}

class _VueListe extends StatelessWidget {
  const _VueListe();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SeanceDetailViewModel>();

    return LigneTable(
      lignes: vm.lignesFiltrees,
      afficherRelais: true,
      estFaite: vm.estFaite,
      onToggle: vm.basculerFait,
      estSelectionnee: vm.estSelectionnee,
      onSelect: vm.basculerSelection,
    );
  }
}

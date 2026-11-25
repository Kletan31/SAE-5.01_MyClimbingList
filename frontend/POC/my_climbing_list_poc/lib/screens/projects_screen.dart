import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/projects_viewmodel.dart';
import 'package:my_climbing_list_poc/widgets/grade_badge.dart';
import 'package:my_climbing_list_poc/widgets/selection_voie_bloc.dart';
import 'package:provider/provider.dart';

class ProjectsScreen extends StatelessWidget {
  const ProjectsScreen({super.key});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (context) =>
            ProjectsViewmodel(context.read<ApiService>())..charger(),
        child: const _ProjectsScreen(),
      );
}

class _ProjectsScreen extends StatelessWidget {
  const _ProjectsScreen();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<ProjectsViewmodel>();

    return SafeArea(
      child: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : Column(
                  spacing: 10,
                  children: [
                    SelectionVoieBloc(
                      selected: vm.type,
                      onChanged: vm.changerType,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(vm.grimpesFiltrees.length == 1
                            ? "${vm.grimpesFiltrees.length} ${vm.type == TypeLigne.voie ? "voie" : "bloc"} en projet"
                            : vm.grimpesFiltrees.length > 0
                                ? "${vm.grimpesFiltrees.length} ${vm.type == TypeLigne.voie ? "voies" : "blocs"} en projet "
                                : "${vm.type == TypeLigne.voie ? "Aucune voie" : "Aucun bloc"} en projet "),
                        Tooltip(
                          triggerMode: TooltipTriggerMode.tap,
                          constraints: const BoxConstraints(maxWidth: 250),
                          showDuration: const Duration(seconds: 5),
                          textAlign: TextAlign.center,
                          child: const Icon(Icons.info_outline),
                          richMessage: TextSpan(children: <TextSpan>[
                            TextSpan(
                              text: 'Voies essayées mais pas enchaînées\n',
                            ),
                            TextSpan(
                              text: 'Astuce',
                              style: TextStyle(fontWeight: FontWeight.bold),
                            ),
                            TextSpan(
                              text:
                                  ' : glissez vers la gauche pour supprimer un projet ',
                            ),
                          ]),
                        ),
                      ],
                    ),
                    Expanded(
                      child: ListView.builder(
                        itemCount: vm.grimpesFiltrees.length,
                        itemBuilder: (_, index) {
                          final item = vm.grimpesFiltrees[index];
                          final salle = vm.salleDeLigne(item.idLigne);
                          final premiereMontee =
                              vm.datePremiereMontee(item.idLigne);
                          final derniereMontee =
                              vm.dateDerniereMontee(item.idLigne);
                          final ligne = vm.lignes.firstWhere(
                            (ligne) => ligne.id == item.idLigne,
                          );

                          return Dismissible(
                              key: ValueKey(item.idGrimpe),
                              direction: DismissDirection.endToStart,
                              background: Container(
                                color: Colors.red,
                                alignment: Alignment.centerRight,
                                padding: const EdgeInsets.only(right: 16),
                                child: const Icon(
                                  Icons.delete,
                                  color: Colors.white,
                                ),
                              ),
                              onDismissed: (_) => vm.supprimer(item.idSeance),
                              child: ExpansionTile(
                                key: PageStorageKey(item),
                                shape: const Border(),
                                collapsedShape: const Border(),
                                tilePadding:
                                    const EdgeInsets.symmetric(horizontal: 16),
                                title: Row(
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Expanded(
                                      flex: 2,
                                      child: Column(
                                        mainAxisSize: MainAxisSize.min,
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            salle?.nom ?? 'Salle inconnue',
                                            style: const TextStyle(
                                              fontStyle: FontStyle.italic,
                                            ),
                                          ),
                                          Text(
                                            "${vm.type == TypeLigne.voie ? "Relais : ${ligne.relais}" : "Secteur : ${ligne.secteur}"} - ${ligne.couleur}",
                                            style: const TextStyle(
                                              color: Colors.grey,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                    Expanded(
                                      child: Center(
                                        child: _BadgeTemporaire(
                                          proprietes: ligne.proprietes,
                                        ),
                                      ),
                                    ),
                                    Expanded(
                                      child: Align(
                                        alignment: Alignment.centerRight,
                                        child: GradeBadge(
                                            cotation: ligne.cotation),
                                      ),
                                    ),
                                  ],
                                ),
                                children: [
                                  _DetailProjet(
                                    type: vm.typeDeLigne(item.idLigne),
                                    dateOuverture: premiereMontee == null
                                        ? 'Inconnue'
                                        : DateFormat('dd MMM yyyy')
                                            .format(premiereMontee),
                                    derniereMontee: derniereMontee == null
                                        ? 'Inconnue'
                                        : DateFormat('dd MMM yyyy')
                                            .format(derniereMontee),
                                    nbMontees: vm.nombreMontees(item.idLigne),
                                  ),
                                ],
                              ));
                        },
                      ),
                    ),
                  ],
                ),
    );
  }
}

class _DetailProjet extends StatelessWidget {
  final TypeLigne type;
  final String dateOuverture;
  final String derniereMontee;
  final int nbMontees;

  const _DetailProjet({
    required this.type,
    required this.dateOuverture,
    required this.derniereMontee,
    required this.nbMontees,
  });

  @override
  Widget build(BuildContext context) => Container(
        color: Colors.grey.shade100,
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Column(
              children: [
                const Text("Ouvert le"),
                Text(
                  dateOuverture,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            Column(
              children: [
                const Text("Dernière montée"),
                Text(
                  derniereMontee,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            Column(
              children: [
                Text(type == TypeLigne.voie ? "Moulinette" : "Montées"),
                Text(
                  "$nbMontees",
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ],
        ),
      );
}

/**
 * Classe temporaire pour afficher les propriétés sous forme de badge.
 */
class _BadgeTemporaire extends StatelessWidget {
  final List<String> proprietes;

  const _BadgeTemporaire({required this.proprietes});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: proprietes
          .map(
            (propriete) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 3,
                  vertical: 1,
                ),
                decoration: BoxDecoration(
                  color: Colors.grey.shade200,
                  borderRadius: BorderRadius.circular(5),
                ),
                child: Text(propriete,
                style: const TextStyle(fontSize: 12)),
              ),
            ),
          )
          .toList(),
    );
  }
}

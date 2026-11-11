import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/projects_viewmodel.dart';
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
              : vm.grimpes.isEmpty
                  ? const Center(child: Text('Aucun projet'))
                  : ListView.builder(
                      itemCount: vm.grimpes.length,
                      itemBuilder: (_, index) {
                        final item = vm.grimpes[index];

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
                              title: Text('Test',
                                  style: const TextStyle(
                                      fontStyle: FontStyle.italic)),
                              subtitle: Text('Relais: '),
                              trailing: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const SizedBox(width: 16),
                                  Text("T"),
                                ],
                              ),
                              children: [
                                const _DetailProjet(
                                  type: Type.voie,
                                  dateOuverture: "19 Sep 2026",
                                  derniereMontee: "12 Oct 2026",
                                  nbMontees: 3,
                                ),
                              ],
                            ));
                      },
                    ),
    );
  }
}

enum Type { voie, bloc }

class _DetailProjet extends StatelessWidget {
  final Type type;
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
                Text(type == Type.voie ? "Moulinette" : "Montées"),
                const Text(
                  "3",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ],
        ),
      );
}

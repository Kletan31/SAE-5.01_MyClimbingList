import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/main.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/seance/ajout_seance_viewmodel.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';

class AjoutSeanceScreen extends StatelessWidget {
  final List<Ligne> lignes; // lignes choisies sur la page précédente
  const AjoutSeanceScreen({super.key, required this.lignes});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (context) =>
            AjoutSeanceViewModel(context.read<ApiService>(), lignes),
        child: const _AjoutSeanceView(),
      );
}

class _AjoutSeanceView extends StatelessWidget {
  const _AjoutSeanceView();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AjoutSeanceViewModel>();

    return Scaffold(
      appBar: const AppHeader(title: 'Ajouter ma séance'),
      body: Column(children: [
        const _DateSelector(),
        const Divider(height: 1),
        Expanded(
          child: ListView.separated(
            itemCount: vm.entrees.length + 1,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (_, i) => i == vm.entrees.length
                ? const _AjouterOuverture()
                : _LigneSeanceCard(
                    key: ValueKey(vm.entrees[i].ligne.id),
                    entree: vm.entrees[i],
                  ),
          ),
        ),
      ]),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: FilledButton(
            // null désactive le bouton pendant l'envoi
            onPressed:
                vm.enregistrement ? null : () => _enregistrer(context, vm),
            child: vm.enregistrement
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2))
                : const Text('Enregistrer ma séance'),
          ),
        ),
      ),
    );
  }
}

Future<void> _enregistrer(BuildContext context, AjoutSeanceViewModel vm) async {
  final ok = await vm.enregistrer();
  if (!context.mounted) return; // l'écran a pu être fermé pendant l'attente
  if (ok) {
    // retour à l'accueil (premier onglet de MainShell)
    Navigator.of(context, rootNavigator: true).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const MainShell()),
      (route) => false,
    );
  } else {
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(vm.erreur ?? 'Erreur')));
  }
}

class _DateSelector extends StatelessWidget {
  const _DateSelector();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AjoutSeanceViewModel>();
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(DateFormat('dd/MM/yyyy').format(vm.date),
            style: Theme.of(context).textTheme.titleMedium),
        IconButton(
          icon: const Icon(Icons.calendar_month),
          onPressed: () => _choisirDate(context, vm),
        ),
      ]),
    );
  }
}

Future<void> _choisirDate(BuildContext context, AjoutSeanceViewModel vm) async {
  final choisie = await showDatePicker(
    context: context,
    initialDate: vm.date,
    firstDate: DateTime(2020),
    lastDate: DateTime.now(), // empêche de sélectionner une date future
  );
  if (choisie != null) vm.changerDate(choisie);
}

class _LigneSeanceCard extends StatelessWidget {
  final LigneSeance entree;
  const _LigneSeanceCard({super.key, required this.entree});

  @override
  Widget build(BuildContext context) {
    final vm = context.read<AjoutSeanceViewModel>();
    final ligne = entree.ligne;
    final titre = ligne.relais != null
        ? 'Relais: ${ligne.relais} – ${ligne.cotation}'
        : ligne.cotation;

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Flexible(
            child: Text(titre,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 8),
          Text('[${ligne.couleur}]',
              style:
                  TextStyle(fontSize: 12, color: Theme.of(context).hintColor)),
          const Spacer(),
          const Tooltip(
            // message: 'Montée : un essai\nTop : essai sans chute\nFlash : premier essai sans chute', // POC
            richMessage: TextSpan(children: <TextSpan>[
              TextSpan(
                text: 'Montée',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              TextSpan(
                text: ' : un essai\n',
              ),
              TextSpan(
                text: 'Top',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              TextSpan(
                text: ' : essai sans chute\n',
              ),
              TextSpan(
                text: 'Flash',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              TextSpan(text: ': premier essai sans chute')
            ]),
            triggerMode: TooltipTriggerMode.tap,
            child: Padding(
                padding: EdgeInsets.all(8), child: Icon(Icons.info_outline)),
          ),
          IconButton(
            icon: const Icon(Icons.delete, color: Colors.red),
            onPressed: () => vm.retirer(entree),
          ),
        ]),
        // POC : moulinette et badge sont en dur
        const Row(children: [
          Text('Moulinette'),
          SizedBox(width: 6),
          _Badge('5|3'),
        ]),
        const SizedBox(height: 8),
        Row(children: [
          _Compteur(
            label: 'Montée',
            valeur: entree.montee,
            onMoins: () => vm.changerMontee(entree, -1),
            onPlus: () => vm.changerMontee(entree, 1),
          ),
          const SizedBox(width: 40),
          _Compteur(
            label: 'Top',
            valeur: entree.top,
            onMoins: () => vm.changerTop(entree, -1),
            onPlus: () => vm.changerTop(entree, 1),
          ),
        ]),
      ]),
    );
  }
}

class _Badge extends StatelessWidget {
  final String texte;
  const _Badge(this.texte);

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
        decoration: BoxDecoration(
          color: Colors.grey.shade300,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(texte,
            style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold)),
      );
}

class _Compteur extends StatelessWidget {
  final String label;
  final int valeur;
  final VoidCallback onMoins, onPlus;

  const _Compteur({
    required this.label,
    required this.valeur,
    required this.onMoins,
    required this.onPlus,
  });

  Widget _bouton(IconData icone, VoidCallback onPressed) => IconButton(
        icon: Icon(icone),
        onPressed: onPressed,
        padding: EdgeInsets.zero,
        constraints: const BoxConstraints.tightFor(width: 36, height: 40),
      );

  @override
  Widget build(BuildContext context) => Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _bouton(Icons.remove, onMoins),
          Column(children: [
            Container(
              width: 48,
              height: 40,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                border: Border.all(color: Theme.of(context).dividerColor),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text('$valeur',
                  style: Theme.of(context).textTheme.titleMedium),
            ),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 12)),
          ]),
          _bouton(Icons.add, onPlus),
        ],
      );
}

class _AjouterOuverture extends StatelessWidget {
  const _AjouterOuverture();

  @override
  Widget build(BuildContext context) => InkWell(
        // On renvoie les lignes encore sélectionnées à la page précédente
        onTap: () => Navigator.pop(
          context,
          context.read<AjoutSeanceViewModel>().lignesSelectionnees,
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(Icons.add_circle,
                color: Theme.of(context).colorScheme.primary),
            const SizedBox(width: 8),
            const Text('Ajouter une ouverture',
                style: TextStyle(fontWeight: FontWeight.bold)),
          ]),
        ),
      );
}

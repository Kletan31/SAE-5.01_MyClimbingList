import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/account/account_viewmodel.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';
import 'package:my_climbing_list_poc/widgets/grade_badge.dart';
import 'package:provider/provider.dart';

const _bleu = Color(0xFF3F51A3);
const _orange = Color(0xFFF08000);

class AccountScreen extends StatelessWidget {
  const AccountScreen({super.key});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (context) =>
            AccountViewModel(context.read<ApiService>())..charger(),
        child: const _AccountView(),
      );
}

class _AccountView extends StatelessWidget {
  const _AccountView();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AccountViewModel>();

    return Scaffold(
      appBar: const AppHeader(title: 'Profile'),
      body: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : vm.user == null
                  ? const Center(child: Text('Utilisateur introuvable'))
                  : ListView(children: [
                      const _BarreActions(),
                      _Identite(nom: vm.nomUtilisateur),
                      const SizedBox(height: 16),
                      _ChoixType(vm: vm),
                      const SizedBox(height: 24),
                      _SalleFavorite(nom: vm.salleFavorite),
                      const SizedBox(height: 16),
                      vm.type == TypeLigne.voie
                          ? _StatsVoie(vm: vm)
                          : _StatsBloc(vm: vm),
                      const Divider(height: 32),
                      _Preferences(
                          profil: vm.profilFavori, style: vm.styleFavori),
                      const SizedBox(height: 16),
                      _Niveau(
                          cotation: vm.cotationMaxi, nbSeances: vm.nbSeances),
                      const SizedBox(height: 16),
                      const _BoutonCarnet(),
                      const SizedBox(height: 24),
                    ]),
    );
  }
}

class _BarreActions extends StatelessWidget {
  const _BarreActions();

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Row(children: [
          // TODO(auth): déconnexion (vider l'utilisateur courant + retour login)
          IconButton(onPressed: () {}, icon: const Icon(Icons.logout)),
          // TODO: Page Suivie
          IconButton(onPressed: () {}, icon: const Icon(Icons.fitness_center)),
          const Spacer(),
          // TODO: choix de la langue (intl : fichiers .arb FR / EN / PT / ES)
          IconButton(onPressed: () {}, icon: const Icon(Icons.language)),
          // TODO: formulaire de retour / signalement de bug
          IconButton(onPressed: () {}, icon: const Icon(Icons.feedback_outlined)),
          // TODO: écran paramètres (compte, notifications)
          IconButton(onPressed: () {}, icon: const Icon(Icons.settings)),
        ]),
      );
}

class _Identite extends StatelessWidget {
  final String nom;
  const _Identite({required this.nom});

  @override
  Widget build(BuildContext context) => Column(children: [
        const CircleAvatar(
          radius: 50,
          backgroundColor: Color(0xFF1B2F55),
          child: Icon(Icons.person, size: 64, color: Colors.white),
        ),
        const SizedBox(height: 8),
        Text(nom,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
      ]);
}

class _ChoixType extends StatelessWidget {
  final AccountViewModel vm;
  const _ChoixType({required this.vm});

  @override
  Widget build(BuildContext context) => Center(
        child: SegmentedButton<TypeLigne>(
          showSelectedIcon: false,
          style: SegmentedButton.styleFrom(
            selectedBackgroundColor: _bleu,
            selectedForegroundColor: Colors.white,
          ),
          segments: const [
            ButtonSegment(value: TypeLigne.voie, label: Text('Voie')),
            ButtonSegment(value: TypeLigne.bloc, label: Text('Bloc')),
          ],
          selected: {vm.type},
          onSelectionChanged: (s) => vm.changerType(s.first),
        ),
      );
}

class _SalleFavorite extends StatelessWidget {
  final String? nom;
  const _SalleFavorite({required this.nom});

  @override
  Widget build(BuildContext context) => Column(children: [
        const Text('Salle préférée', style: TextStyle(fontSize: 18)),
        const SizedBox(height: 4),
        Text(nom ?? '-',
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800)),
      ]);
}

class _StatsVoie extends StatelessWidget {
  final AccountViewModel vm;
  const _StatsVoie({required this.vm});

  @override
  Widget build(BuildContext context) => IntrinsicHeight(
        child: Row(children: [
          Expanded(child: _BlocStats(titre: 'Moulinette', stats: vm.moulinette)),
          const VerticalDivider(width: 1),
          Expanded(child: _BlocStats(titre: 'Tête', stats: vm.tete)),
        ]),
      );
}

class _StatsBloc extends StatelessWidget {
  final AccountViewModel vm;
  const _StatsBloc({required this.vm});

  @override
  Widget build(BuildContext context) =>
      _BlocStats(titre: 'Ascensions', stats: vm.bloc);
}

class _BlocStats extends StatelessWidget {
  final String titre;
  final StatsGrimpe stats;
  const _BlocStats({required this.titre, required this.stats});

  @override
  Widget build(BuildContext context) => Column(children: [
        Text(titre, style: const TextStyle(fontSize: 18)),
        const SizedBox(height: 8),
        Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
          _Chiffre(valeur: stats.top, label: 'Top'),
          _Chiffre(valeur: stats.flash, label: 'Flash'),
        ]),
      ]);
}

class _Chiffre extends StatelessWidget {
  final int valeur;
  final String label;
  const _Chiffre({required this.valeur, required this.label});

  @override
  Widget build(BuildContext context) => Column(children: [
        Text('$valeur',
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800)),
        Text(label, style: const TextStyle(fontSize: 11)),
      ]);
}

class _Preferences extends StatelessWidget {
  final String? profil, style;
  const _Preferences({required this.profil, required this.style});

  @override
  Widget build(BuildContext context) => IntrinsicHeight(
        child: Row(children: [
          Expanded(child: _Preference(titre: 'Profil favori', valeur: profil)),
          const VerticalDivider(width: 1),
          Expanded(child: _Preference(titre: 'Style favori', valeur: style)),
        ]),
      );
}

class _Preference extends StatelessWidget {
  final String titre;
  final String? valeur;
  const _Preference({required this.titre, required this.valeur});

  @override
  Widget build(BuildContext context) => Column(children: [
        Text(titre, style: const TextStyle(fontSize: 18)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: BoxDecoration(
            color: const Color(0xFF2E2E2E),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Text(valeur ?? '-',
              style: const TextStyle(
                  color: Colors.white,
                  fontSize: 11,
                  fontWeight: FontWeight.w700)),
        ),
      ]);
}

class _Niveau extends StatelessWidget {
  final String? cotation;
  final int nbSeances;
  const _Niveau({required this.cotation, required this.nbSeances});

  @override
  Widget build(BuildContext context) => Column(children: [
        const Text('Grade', style: TextStyle(fontSize: 18)),
        const SizedBox(height: 8),
        GradeBadge(cotation: cotation ?? '-', size: 68, fontSize: 24),
        const SizedBox(height: 6),
        Text('$nbSeances séances enregistrées',
            style: const TextStyle(fontSize: 11)),
      ]);
}

class _BoutonCarnet extends StatelessWidget {
  const _BoutonCarnet();

  @override
  Widget build(BuildContext context) => Center(
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: _orange,
            foregroundColor: Colors.white,
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
          ),
          // TODO: ouvrir le carnet complet (liste de toutes les séances,
          // filtrable). Aujourd'hui c'est l'onglet Home qui l'affiche.
          onPressed: () {},
          child: const Text('Mon Carnet',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
        ),
      );
}
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../services/api_service.dart';
import '../../viewmodels/home/home_viewmodel.dart';
import 'package:intl/intl.dart';
import '../../widgets/grade_badge.dart';
import 'session_detail_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (context) =>
            HomeViewModel(context.read<ApiService>())..charger(),
        child: const _HomeView(),
      );
}

class _HomeView extends StatelessWidget {
  const _HomeView();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<HomeViewModel>();

    return SafeArea(
      child: vm.chargement
          ? const Center(child: CircularProgressIndicator())
          : vm.erreur != null
              ? Center(child: Text('Erreur : ${vm.erreur}'))
              : Column(children: [
                  _WeeklyOverview(
                    sessions: vm.nbSessionsSemaine,
                    ascents: vm.ascentsSemaine,
                    tops: vm.topsSemaine,
                    max: vm.maxSemaine,
                  ),
                  const Divider(height: 1, thickness: 1),
                  Expanded(
                    child: vm.sessions.isEmpty
                        ? const Center(child: Text('Aucune séance'))
                        : ListView.separated(
                            itemCount: vm.sessions.length,
                            separatorBuilder: (_, __) =>
                                const Divider(height: 1),
                            itemBuilder: (_, i) =>
                                _SessionTile(session: vm.sessions[i]),
                          ),
                  ),
                ]),
    );
  }
}

class _WeeklyOverview extends StatelessWidget {
  final int sessions, ascents, tops;
  final String? max;
  const _WeeklyOverview({
    required this.sessions,
    required this.ascents,
    required this.tops,
    required this.max,
  });

  @override
  Widget build(BuildContext context) => Column(children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: const Color(0xFF2E2E2E),
            borderRadius: BorderRadius.circular(4),
          ),
          child: const Text('Weekly overview',
              style: TextStyle(
                  color: Colors.white,
                  fontSize: 11,
                  fontWeight: FontWeight.w600)),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
            _Stat(valeur: '$sessions', label: 'Session'),
            _Stat(valeur: '$ascents', label: 'Ascent'),
            const SizedBox(height: 32, child: VerticalDivider(width: 1)),
            _Stat(valeur: '$tops', label: 'Top'),
            _Stat(valeur: max ?? '-', label: 'Max'),
          ]),
        ),
      ]);
}

class _SessionTile extends StatelessWidget {
  final Session session;
  const _SessionTile({required this.session});

  String get _date => DateFormat('dd MMM yyyy').format(session.date);


  @override
  Widget build(BuildContext context) => InkWell(
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => SessionDetailScreen(session: session),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(children: [
            Expanded(
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(children: [
                      Flexible(
                        child: Text(session.nom,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                                fontSize: 16, fontWeight: FontWeight.w700)),
                      ),
                      const SizedBox(width: 6),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 6, vertical: 1),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade200,
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(session.estBloc ? 'Boulder' : 'Route',
                            style: const TextStyle(
                                fontSize: 9, color: Colors.black87)),
                      ),
                    ]),
                    const SizedBox(height: 6),
                    Text(_date,
                        style: const TextStyle(
                            fontSize: 14,
                            fontStyle: FontStyle.italic,
                            fontWeight: FontWeight.w600)),
                  ]),
            ),
            _Stat(valeur: '${session.ascents}', label: 'Ascent'),
            const SizedBox(height: 40, child: VerticalDivider(width: 24)),
            _Stat(valeur: '${session.tops}', label: 'Top'),
            const SizedBox(width: 20),
            GradeBadge(cotation: session.max, label: 'Max'),
          ]),
        ),
      );
}

class _Stat extends StatelessWidget {
  final String valeur, label;
  const _Stat({required this.valeur, required this.label});

  @override
  Widget build(BuildContext context) => Column(children: [
        Text(valeur,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ]);
}
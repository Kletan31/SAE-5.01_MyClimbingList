import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../viewmodels/home/home_viewmodel.dart';
import '../../viewmodels/home/session_detail_viewmodel.dart';
import '../../widgets/app_header.dart';
import '../../widgets/grade_badge.dart';

class SessionDetailScreen extends StatelessWidget {
  final Session session;
  const SessionDetailScreen({super.key, required this.session});

  @override
  Widget build(BuildContext context) => ChangeNotifierProvider(
        create: (_) => SessionDetailViewModel(session),
        child: const _SessionDetailView(),
      );
}

class _SessionDetailView extends StatelessWidget {
  const _SessionDetailView();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SessionDetailViewModel>();

    return Scaffold(
      appBar: AppHeader(title: vm.titre),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Column(children: [
            Text(vm.nom,
                style:
                    const TextStyle(fontSize: 12, fontWeight: FontWeight.w700)),
            Text(vm.date,
                style: const TextStyle(
                    fontSize: 10, fontStyle: FontStyle.italic)),
          ]),
        ),
        _Histogramme(vm: vm),
        const Divider(thickness: 1),
        Expanded(
          child: ListView.separated(
            itemCount: vm.lignes.length,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (_, i) => _LigneTile(vm: vm, index: i),
          ),
        ),
      ]),
    );
  }
}

class _Histogramme extends StatelessWidget {
  final SessionDetailViewModel vm;
  const _Histogramme({required this.vm});

  @override
  Widget build(BuildContext context) => SizedBox(
        height: 220,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
            for (final c in cotationsHistogramme)
              Expanded(
                child: Column(mainAxisAlignment: MainAxisAlignment.end, children: [
                  Expanded(
                    child: Align(
                      alignment: Alignment.bottomCenter,
                      child: FractionallySizedBox(
                        heightFactor: vm.hauteurBarre(c),
                        child: Container(width: 8, color: Colors.lightGreen),
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
      );
}

class _LigneTile extends StatelessWidget {
  final SessionDetailViewModel vm;
  final int index;
  const _LigneTile({required this.vm, required this.index});

  @override
  Widget build(BuildContext context) {
    final l = vm.lignes[index];
    return ListTile(
      title: Text(vm.libelleRelais(l),
          style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic)),
      subtitle: Text('${vm.libelleProprietes(l)}\n${vm.libelleResultat(l)}'),
      isThreeLine: true,
      trailing: GradeBadge(
        cotation: vm.libelleCotation(l),
        size: 40,
        fontSize: 14,
      ),
    );
  }
}
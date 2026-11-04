import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/viewmodels/carnet_viewmodel.dart';
import 'package:my_climbing_list_poc/widgets/carnet_ligne_tile.dart';
import 'package:provider/provider.dart';

class CarnetScreen extends StatelessWidget {
  final bool showHeader;

  const CarnetScreen({super.key, this.showHeader = true});

  @override
  Widget build(BuildContext context) {
    final body = ChangeNotifierProvider(
      create: (context) =>
          CarnetViewModel(context.read<ApiService>())..charger(),
      child: const _CarnetBody(),
    );

    return showHeader
        ? Scaffold(
            appBar: const _CarnetHeader(),
            body: body,
          )
        : body;
  }
}

class _CarnetHeader extends StatelessWidget implements PreferredSizeWidget {
  const _CarnetHeader();

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) => AppBar(
        leading: IconButton(
          onPressed: () => Navigator.of(context).pop(),
          icon: const Icon(Icons.arrow_back_ios_new, size: 20),
        ),
        title: Transform(
          alignment: Alignment.center,
          transform: Matrix4.skewX(-0.3),
          child: Container(
            color: const Color(0xFFF57C00),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
            child: const Text(
              'Carnet',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(LucideIcons.circleUser, size: 28),
            onPressed: () {},
          ),
        ],
      );
}

class _CarnetBody extends StatelessWidget {
  const _CarnetBody();

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<CarnetViewModel>();
    if (vm.chargement) {
      return const Center(child: CircularProgressIndicator());
    }
    if (vm.erreur != null) {
      return Center(child: Text('Erreur : ${vm.erreur}'));
    }

    return SafeArea(
      child: Column(
        children: [
          _Filtres(vm: vm),
          Expanded(
            child: vm.items.isEmpty
                ? const Center(child: Text('Aucune ascension pour ce filtre.'))
                : ListView.separated(
                    itemCount: vm.items.length,
                    separatorBuilder: (_, __) =>
                        const Divider(height: 1, color: Color(0xFF333333)),
                    itemBuilder: (_, index) {
                      final item = vm.items[index];
                      return CarnetLigneTile(
                        ligne: item.ligne,
                        grimpe: item.grimpe,
                        date: item.date,
                        salle: item.salle,
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class _Filtres extends StatelessWidget {
  final CarnetViewModel vm;
  const _Filtres({required this.vm});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 16, bottom: 14),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _FilterButton(
                icon: LucideIcons.zap,
                color: const Color(0xFFFFB300),
                selected: vm.flashActif,
                onPressed: vm.changerFlash,
              ),
              const SizedBox(width: 48),
              _FilterButton(
                icon: LucideIcons.arrowUp,
                color: const Color(0xFFA8D63B),
                selected: vm.topActif,
                onPressed: vm.changerTop,
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            '${vm.items.length} ${vm.items.length > 1 ? 'voies réalisées' : 'voie réalisée'}',
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
        ],
      ),
    );
  }
}

class _FilterButton extends StatelessWidget {
  final IconData icon;
  final Color color;
  final bool selected;
  final VoidCallback onPressed;

  const _FilterButton({
    required this.icon,
    required this.color,
    required this.selected,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) => Material(
        color: selected ? color : const Color(0xFF292D2F),
        shape: const CircleBorder(),
        child: InkWell(
          customBorder: const CircleBorder(),
          onTap: onPressed,
          child: SizedBox(
            width: 34,
            height: 34,
            child: Icon(icon, color: Colors.white, size: 24),
          ),
        ),
      );
}

import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import '../screens/account_screen.dart';

class AppHeader extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  const AppHeader({super.key, required this.title});

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    final accent = Theme.of(context).colorScheme.primary;

    return AppBar(
      centerTitle: true,
      title: Transform(
        alignment: Alignment.center,
        transform: Matrix4.skewX(-0.3),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
          color: accent,
          child: Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w800,
            ),
          ),
        ),
      ),
      actions: [
        IconButton(
          icon: const Icon(LucideIcons.circleUser),
          iconSize: 28,
          onPressed: () => Navigator.of(context).push(
            MaterialPageRoute(builder: (_) => const AccountScreen()),
          ),
        ),
      ],
    );
  }
}

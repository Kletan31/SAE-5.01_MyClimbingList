import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';

class TabNavigator extends StatelessWidget {
  final GlobalKey<NavigatorState> navigatorKey;
  final String titre;
  final Widget racine;

  const TabNavigator({
    super.key,
    required this.navigatorKey,
    required this.titre,
    required this.racine,
  });

  @override
  Widget build(BuildContext context) => Navigator(
        key: navigatorKey,
        onGenerateRoute: (_) => MaterialPageRoute(
          builder: (_) => Scaffold(
            appBar: AppHeader(title: titre),
            body: racine,
          ),
        ),
      );
}

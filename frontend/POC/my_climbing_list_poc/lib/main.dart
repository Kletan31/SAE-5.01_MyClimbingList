import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/services/mock_api_service.dart';
import 'package:my_climbing_list_poc/widgets/tab_navigator.dart';
import 'package:provider/provider.dart';
import 'screens/home/home_screen.dart';
import 'screens/contest_screen.dart';
import 'screens/seance/seance_screen.dart';
import 'screens/projects_screen.dart';
import 'screens/profile_screen.dart';
import 'theme/app_theme.dart';
import 'widgets/app_header.dart';

void main() {
  runApp(
    Provider<ApiService>(
      create: (_) => MockApiService(),
      child: const MyClimbingListApp(),
    ),
  );
}

class MyClimbingListApp extends StatelessWidget {
  const MyClimbingListApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Climbing List',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      home: const MainShell(),
    );
  }
}

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int index = 0;

  final titles = const ['Accueil', 'Contests', 'Séances', 'Projets', 'Stats'];

  final _navKeys = List.generate(5, (_) => GlobalKey<NavigatorState>());

  late final List<Widget> _tabs = [
    TabNavigator(
        navigatorKey: _navKeys[0],
        titre: titles[0],
        racine: const HomeScreen()),
    TabNavigator(
        navigatorKey: _navKeys[1],
        titre: titles[1],
        racine: const ContestScreen()),
    TabNavigator(
        navigatorKey: _navKeys[2],
        titre: titles[2],
        racine: const SeanceScreen()),
    TabNavigator(
        navigatorKey: _navKeys[3],
        titre: titles[3],
        racine: const ProjectsScreen()),
    TabNavigator(
        navigatorKey: _navKeys[4],
        titre: titles[4],
        racine: const ProfileScreen()), // à remplacer par StatsScreen()
  ];

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (didPop) return;
        final nav = _navKeys[index].currentState!;
        if (nav.canPop()) {
          nav.pop();
        } else if (index != 0) {
          setState(() => index = 0);
        } else {
          SystemNavigator.pop();
        }
      },
      child: Scaffold(
        body: IndexedStack(index: index, children: _tabs),
        bottomNavigationBar: NavigationBar(
          selectedIndex: index,
          onDestinationSelected: (value) {
            if (value == index) {
              _navKeys[value].currentState?.popUntil((r) => r.isFirst);
            } else {
              setState(() => index = value);
            }
          },
          destinations: const [
            NavigationDestination(
                icon: Icon(LucideIcons.house), label: 'Accueil'),
            NavigationDestination(
                icon: Icon(LucideIcons.swords), label: 'Contests'),
            NavigationDestination(
                icon: Icon(LucideIcons.circlePlus), label: 'Séances'),
            NavigationDestination(
                icon: Icon(LucideIcons.listChecks), label: 'Projets'),
            NavigationDestination(
                icon: Icon(LucideIcons.chartLine), label: 'Stats'),
          ],
        ),
      ),
    );
  }
}

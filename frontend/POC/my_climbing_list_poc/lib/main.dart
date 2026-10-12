import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/services/mock_api_service.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
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

  final pages = const [
    HomeScreen(),
    ContestScreen(),
    SeanceScreen(),
    ProjectsScreen(),
    ProfileScreen(), // à remplacer par StatsScreen()
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppHeader(title: titles[index]),
      body: IndexedStack(index: index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (value) => setState(() => index = value),
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
    );
  }
}

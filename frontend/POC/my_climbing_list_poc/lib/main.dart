import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/topo_screen.dart';
import 'screens/session_screen.dart';
import 'screens/projects_screen.dart';
import 'screens/profile_screen.dart';
import 'theme/app_theme.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';

void main() {
  runApp(const MyClimbingListApp());
}

class MyClimbingListApp extends StatefulWidget {
  const MyClimbingListApp({super.key});
  @override
  State<MyClimbingListApp> createState() => _MyClimbingListAppState();
}

class _MyClimbingListAppState extends State<MyClimbingListApp> {
  int index = 0;
  final pages = const [
    HomeScreen(),
    TopoScreen(),
    SessionScreen(),
    ProjectsScreen(),
    ProfileScreen()
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Climbing List',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      home: Scaffold(
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
      ),
    );
  }
}

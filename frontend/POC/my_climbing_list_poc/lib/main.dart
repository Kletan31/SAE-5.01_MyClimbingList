import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/topo_screen.dart';
import 'screens/session_screen.dart';
import 'screens/projects_screen.dart';
import 'screens/profile_screen.dart';
import 'theme/app_theme.dart';

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
  final pages = const [HomeScreen(), TopoScreen(), SessionScreen(), ProjectsScreen(), ProfileScreen()];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Climbing List',
      theme: AppTheme.light,
      home: Scaffold(
        body: IndexedStack(index: index, children: pages),
        bottomNavigationBar: NavigationBar(
          selectedIndex: index,
          onDestinationSelected: (value) => setState(() => index = value),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Accueil'),
            NavigationDestination(icon: Icon(Icons.grid_view_outlined), selectedIcon: Icon(Icons.grid_view), label: 'Contests'),
            NavigationDestination(icon: Icon(Icons.add_circle_outline), selectedIcon: Icon(Icons.add_circle), label: 'Séance'),
            NavigationDestination(icon: Icon(Icons.flag_outlined), selectedIcon: Icon(Icons.flag), label: 'Projets'),
            NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Stats'),
          ],
        ),
      ),
    );
  }
}

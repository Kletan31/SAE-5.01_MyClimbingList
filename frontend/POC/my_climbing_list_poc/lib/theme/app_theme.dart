import 'package:flutter/material.dart';

class AppTheme {
  static const Color accent = Color(0xFFF57C00); // orange
  static const Color pageAccent = Color.fromARGB(255, 63, 81, 163); // accent bleu sur certains éléments
  static const Color tagRouge = Colors.red;
  static const Color tagViolet = Colors.purple;
  static const Color tagBleu = Colors.blue;
  static const Color tagBleuClair = Colors.lightBlue;
  static const Color tagDefaut = Color(0xFF333333);

  static Color couleurTag(String p) {
    final v = p.toLowerCase();
    //POC: Verifier les prorpieter de Ré (A quoi sert-il)
    if (v.contains('rési')) return tagRouge;
    if (v.contains('conti')) return tagBleu;
    if (v.contains('bloc')) return tagViolet;
    if (v.contains('voie')) return tagBleuClair;
    return tagDefaut;
  }

  static const Map<String, Color> couleursLigne = {
    'orange': Colors.orange,
    'vert': Colors.green,
    'rouge': Colors.red,
    'mauve': Colors.purple,
    'violet': Colors.deepPurple,
    'bleu': Colors.blue,
    'marron': Colors.brown,
    'gris': Colors.grey,
    'noir': Colors.black,
    'blanc': Colors.white,
    'jaune': Colors.yellow,
    'rose': Colors.pink,
  };

  static Color couleurLigne(String nom) {
    var n = nom.trim().toLowerCase();
    if (n.endsWith('e') && n != 'rose') n = n.substring(0, n.length - 1);
    return couleursLigne[n] ?? Colors.grey;
  }

  static ThemeData light = _build(
    const ColorScheme.light(
      primary: accent,
      onPrimary: Colors.white,
      secondary: accent,
      surface: Colors.white,
      onSurface: Colors.black87,
    ),
    inactive: Colors.black87,
  );

  static ThemeData dark = _build(
    const ColorScheme.dark(
      primary: accent,
      onPrimary: Colors.black,
      secondary: accent,
      surface: Colors.black,
      onSurface: Colors.white,
    ),
    inactive: Colors.white70,
  );

  static ThemeData _build(ColorScheme scheme, {required Color inactive}) {
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: scheme.surface,
      appBarTheme: AppBarTheme(
        backgroundColor: scheme.surface,
        foregroundColor: scheme.onSurface,
        surfaceTintColor: Colors.transparent,
        elevation: 0,
      ),
      cardTheme: CardThemeData(
        color: scheme.surface,
        surfaceTintColor: Colors.transparent,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: scheme.surface,
        surfaceTintColor: Colors.transparent,
        indicatorColor: Colors.transparent, // pas de pastille
        iconTheme: WidgetStateProperty.resolveWith((states) => IconThemeData(
              color: states.contains(WidgetState.selected) ? accent : inactive,
            )),
        labelTextStyle: WidgetStateProperty.resolveWith((states) => TextStyle(
              fontSize: 12,
              color: states.contains(WidgetState.selected) ? accent : inactive,
            )),
      ),
    );
  }
}

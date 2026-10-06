import 'package:flutter/material.dart';

class AppTheme {
  static const Color accent = Color(0xFFF57C00); // orange

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

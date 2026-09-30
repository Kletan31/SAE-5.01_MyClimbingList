import 'package:flutter/material.dart';

class AppTheme {
  static final light = ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.deepOrange,
    scaffoldBackgroundColor: const Color(0xFFF7F7F7),
    cardTheme: const CardThemeData(margin: EdgeInsets.zero, elevation: 0),
  );
}

import 'package:flutter/material.dart';
import '../viewmodels/home/home_viewmodel.dart' show niveauCotation;

/// Rond de cotation coloré selon le niveau, avec un label optionnel dessous
/// (ex. "Max"). Réutilisable partout où une cotation est affichée.
class GradeBadge extends StatelessWidget {
  final String? cotation;
  final String? label;
  final double size;
  final double fontSize;

  const GradeBadge({
    super.key,
    required this.cotation,
    this.label,
    this.size = 36,
    this.fontSize = 12,
  });

  static Color couleurPour(String? cotation) {
    final n = cotation == null ? -1 : niveauCotation(cotation);
    if (n < 0) return Colors.grey;
    if (n < 60) return Colors.green;
    if (n < 66) return Colors.lightBlue; // 6a .. 6b+
    if (n < 70) return Colors.orange; // 6c .. 6c+
    return Colors.red; // 7a et +
  }

  @override
  Widget build(BuildContext context) => Column(mainAxisSize: MainAxisSize.min, children: [
        Container(
          width: size,
          height: size,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: couleurPour(cotation), width: 2.5),
          ),
          child: Text(cotation ?? '-',
              style: TextStyle(fontSize: fontSize, fontWeight: FontWeight.w700)),
        ),
        if (label != null) ...[
          const SizedBox(height: 2),
          Text(label!, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ],
      ]);
}
import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/theme/app_theme.dart';

class CouleurLigne extends StatelessWidget {
  final String couleur;
  const CouleurLigne({super.key, required this.couleur});

  @override
  Widget build(BuildContext context) => Text(
        couleur,
        style: const TextStyle(fontStyle: FontStyle.italic),
      );
}

// Une étiquette (bloc, dalle, réglettes...).
class TagPropriete extends StatelessWidget {
  final String label;
  const TagPropriete(this.label, {super.key});

  @override
  Widget build(BuildContext context) => Container(
        constraints: const BoxConstraints(maxWidth: 90),
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
        decoration: BoxDecoration(
          color: AppTheme.couleurTag(label),
          borderRadius: BorderRadius.circular(5),
        ),
        child: Text(label,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
                color: Colors.white,
                fontSize: 10,
                fontWeight: FontWeight.bold)),
      );
}

// Étiquettes : type (bloc) puis propriétés.
class ProprietesTags extends StatelessWidget {
  final Ligne ligne;
  final int? maxTags;
  final WrapAlignment alignment;
  final bool afficherType;
  const ProprietesTags({
    super.key,
    required this.ligne,
    this.maxTags,
    this.alignment = WrapAlignment.center,
    this.afficherType = true,
  });

  @override
  Widget build(BuildContext context) {
    final tags = <String>[
      if (afficherType && ligne.type == 'bloc') 'bloc',
      ...ligne.proprietes,
    ];
    final visibles = maxTags == null ? tags : tags.take(maxTags!).toList();
    return Wrap(
      alignment: alignment,
      spacing: 4,
      runSpacing: 3,
      children: [for (final t in visibles) TagPropriete(t)],
    );
  }
}
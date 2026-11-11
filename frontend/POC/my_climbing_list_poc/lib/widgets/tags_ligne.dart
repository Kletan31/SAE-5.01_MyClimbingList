import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';

Color couleurLigne(String nom) {
  var n = nom.trim().toLowerCase();
  if (n.endsWith('e') && n != 'rose') n = n.substring(0, n.length - 1);
  switch (n) {
    case 'orang':
    case 'orange':
      return const Color(0xFFFF9800);
    case 'vert':
      return const Color(0xFF4CAF50);
    case 'roug':
    case 'rouge':
      return const Color(0xFFE53935);
    case 'mauv':
    case 'mauve':
      return const Color(0xFF9C6ADE);
    case 'violet':
      return const Color(0xFF7B1FA2);
    case 'bleu':
      return const Color(0xFF1E88E5);
    case 'marron':
      return const Color(0xFF795548);
    case 'gris':
      return const Color(0xFF9E9E9E);
    case 'noir':
      return Colors.black;
    case 'blanc':
      return Colors.white;
    case 'jaun':
    case 'jaune':
      return const Color(0xFFFDD835);
    case 'rose':
      return const Color(0xFFEC407A);
    default:
      return Colors.grey;
  }
}

// Nom de la couleur de la ligne (ex : Orange), sans pastille.
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

  static Color couleurPour(String p) {
    final v = p.toLowerCase();
    if (v.contains('ré') || v.contains('top')) return Colors.red;
    if (v.contains('bloc')) return Colors.purple;
    if (v.contains('conti') || v.contains('voie')) return Colors.blue;
    return const Color(0xFF333333);
  }

  @override
  Widget build(BuildContext context) => Container(
        constraints: const BoxConstraints(maxWidth: 90),
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
        decoration: BoxDecoration(
          color: couleurPour(label),
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
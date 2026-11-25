import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/widgets/grade_badge.dart';
import 'package:my_climbing_list_poc/widgets/tags_ligne.dart';

class SessionLigneTile extends StatefulWidget {
  final Ligne ligne;
  final Grimpe grimpe;

  const SessionLigneTile(
      {super.key, required this.ligne, required this.grimpe});

  @override
  State<SessionLigneTile> createState() => _SessionLigneTileState();
}

class _SessionLigneTileState extends State<SessionLigneTile> {
  bool _ouvert = false;

  Ligne get ligne => widget.ligne;
  Grimpe get grimpe => widget.grimpe;

  @override
  Widget build(BuildContext context) => Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => setState(() => _ouvert = !_ouvert),
          child: Column(children: [
            _principale(),
            AnimatedCrossFade(
              duration: const Duration(milliseconds: 180),
              crossFadeState: _ouvert
                  ? CrossFadeState.showSecond
                  : CrossFadeState.showFirst,
              firstChild: const SizedBox(width: double.infinity),
              secondChild: _details(),
            ),
          ]),
        ),
      );

  Widget _principale() => Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          child: Row(children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Relais: ${ligne.relais ?? '-'}',
                      style: const TextStyle(
                          fontSize: 13, fontStyle: FontStyle.italic)),
                  const SizedBox(height: 2),
                  Text(ligne.couleur.isEmpty ? '-' : ligne.couleur,
                      style: const TextStyle(
                          fontSize: 13, fontStyle: FontStyle.italic)),
                ],
              ),
            ),
            if (grimpe.top > 0)
              const Icon(Icons.arrow_upward,
                  color: Color(0xFFA8D63B), size: 27),
            if (grimpe.flash)
              const Padding(
                padding: EdgeInsets.only(left: 8),
                child: Icon(Icons.bolt, color: Color(0xFFFFA800), size: 28),
              ),
            const SizedBox(width: 16),
            GradeBadge(cotation: ligne.cotation, size: 44, fontSize: 14),
          ]),
        );

  Widget _details() => Container(
          width: double.infinity,
          color: const Color(0xFFF7F7F7),
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: Row(children: [
            _Colonne('Style', TagPropriete(ligne.type)),
            _Colonne(
              'Profil',
              ProprietesTags(ligne: ligne, afficherType: false),
            ),
            _Colonne('Montée', Text('${grimpe.montee}',
                style: const TextStyle(fontSize: 12))),
            _Colonne('Top', Text('${grimpe.top}',
                style: const TextStyle(fontSize: 12))),
          ]),
        );
}

class _Colonne extends StatelessWidget {
  final String titre;
  final Widget contenu;
  const _Colonne(this.titre, this.contenu);

  @override
  Widget build(BuildContext context) => Expanded(
        child: Column(children: [
          Text(titre, style: const TextStyle(fontSize: 12)),
          const SizedBox(height: 4),
          contenu,
        ]),
      );
}
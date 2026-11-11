import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/widgets/grade_badge.dart';
import 'package:my_climbing_list_poc/widgets/propriete_info.dart';

class CarnetLigneTile extends StatefulWidget {
  final Ligne ligne;
  final Grimpe grimpe;
  final DateTime date;
  final String salle;

  const CarnetLigneTile({
    super.key,
    required this.ligne,
    required this.grimpe,
    required this.date,
    required this.salle,
  });

  @override
  State<CarnetLigneTile> createState() => _CarnetLigneTileState();
}

class _CarnetLigneTileState extends State<CarnetLigneTile> {
  bool _ouvert = false;

  @override
  Widget build(BuildContext context) => Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => setState(() => _ouvert = !_ouvert),
          child: Column(
            children: [
              SizedBox(height: 78, child: _lignePrincipale()),
              AnimatedCrossFade(
                duration: const Duration(milliseconds: 180),
                crossFadeState: _ouvert
                    ? CrossFadeState.showSecond
                    : CrossFadeState.showFirst,
                firstChild: const SizedBox(height: 0),
                secondChild: _details(),
              ),
            ],
          ),
        ),
      );

  Widget _lignePrincipale() => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Row(
          children: [
            Expanded(
              flex: 5,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _date(context, widget.date),
                    style: const TextStyle(
                        fontSize: 18, fontWeight: FontWeight.w700),
                  ),
                  Text(
                    widget.salle,
                    style: const TextStyle(
                        fontSize: 17, fontStyle: FontStyle.italic),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
            SizedBox(
              width: 56,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (widget.grimpe.top > 0)
                    const Icon(LucideIcons.arrowUp,
                        color: Color(0xFFA8D63B), size: 27),
                  if (widget.grimpe.flash)
                    const Icon(LucideIcons.zap,
                        color: Color(0xFFFFA800), size: 25),
                ],
              ),
            ),
            SizedBox(
              width: 76,
              child: ProprietesTags(
                ligne: widget.ligne,
                maxTags: 2,
                alignment: WrapAlignment.end,
              ),
            ),
            const SizedBox(width: 4),
            GradeBadge(cotation: widget.ligne.cotation, size: 44, fontSize: 14),
          ],
        ),
      );

  Widget _details() => Container(
        height: 38,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        color: const Color(0xFFF7F7F7),
        child: Row(
          children: [
            Expanded(
              child: Row(children: [
                Text(
                  'Relais : ${widget.ligne.relais ?? '-'}',
                  style: const TextStyle(
                      fontSize: 12, fontStyle: FontStyle.italic),
                ),
                const SizedBox(width: 10),
                CouleurLigne(couleur: widget.ligne.couleur),
              ]),
            ),
            _DetailValue(
              label: _labels.montee,
              value: widget.grimpe.montee,
            ),
            const SizedBox(width: 28),
            _DetailValue(
              label: _labels.top,
              value: widget.grimpe.top,
            ),
          ],
        ),
      );

  String _date(BuildContext context, DateTime date) =>
      MaterialLocalizations.of(context).formatMediumDate(date);

}

const _labels = (montee: 'Montée', top: 'Top');

class _DetailValue extends StatelessWidget {
  final String label;
  final int value;

  const _DetailValue({required this.label, required this.value});

  @override
  Widget build(BuildContext context) => Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(label, style: const TextStyle(fontSize: 12)),
          Text('$value', style: const TextStyle(fontSize: 12)),
        ],
      );
}
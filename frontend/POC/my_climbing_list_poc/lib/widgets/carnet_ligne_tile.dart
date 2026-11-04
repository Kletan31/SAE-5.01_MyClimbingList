import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:my_climbing_list_poc/models/grimpe_model.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/widgets/grade_badge.dart';

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
                    _date(widget.date),
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
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  for (final property in widget.ligne.proprietes.take(2))
                    _Tag(label: property, color: _propertyColor(property)),
                ],
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
              child: Text(
                'Relais : ${widget.ligne.relais ?? '-'}'
                '${widget.ligne.relais == null ? '' : ' - ${widget.ligne.couleur}'}',
                style:
                    const TextStyle(fontSize: 12, fontStyle: FontStyle.italic),
              ),
            ),
            _DetailValue(label: 'Montée', value: widget.grimpe.montee),
            const SizedBox(width: 28),
            _DetailValue(label: 'Top', value: widget.grimpe.top),
          ],
        ),
      );

  String _date(DateTime date) =>
      '${date.day.toString().padLeft(2, '0')} ${_months[date.month - 1]} ${date.year}';

  static const _months = [
    'Jan',
    'Fév',
    'Mar',
    'Avr',
    'Mai',
    'Juin',
    'Juil',
    'Aoû',
    'Sep',
    'Oct',
    'Nov',
    'Déc'
  ];

  Color _propertyColor(String property) {
    final value = property.toLowerCase();
    if (value.contains('ré') || value.contains('top')) return Colors.red;
    if (value.contains('bloc')) return Colors.purple;
    if (value.contains('conti')) return Colors.blue;
    return const Color(0xFF333333);
  }
}

class _DetailValue extends StatelessWidget {
  final String label;
  final int value;

  const _DetailValue({required this.label, required this.value});

  @override
  Widget build(BuildContext context) => Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(label, style: const TextStyle(fontSize: 12)),
          Text('$value | ${value > 0 ? 1 : 0}',
              style: const TextStyle(fontSize: 12)),
        ],
      );
}

class _Tag extends StatelessWidget {
  final String label;
  final Color color;

  const _Tag({required this.label, required this.color});

  @override
  Widget build(BuildContext context) => Container(
        constraints: const BoxConstraints(maxWidth: 72),
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          label,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
              color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
        ),
      );
}

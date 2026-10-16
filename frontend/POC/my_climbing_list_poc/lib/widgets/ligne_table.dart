import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';

const double _largeurCase = 40;
const int _flexProprietes = 3;
const int _flexRelais = 2;
const int _flexCotation = 2;
const int _flexCouleur = 3;

class LigneTable extends StatelessWidget {
  final List<Ligne> lignes;
  final bool afficherRelais;
  final bool Function(int ligneId) estFaite;
  final void Function(int ligneId) onToggle;
  final bool Function(int ligneId) estSelectionnee;
  final void Function(int ligneId) onSelect;

  const LigneTable(
      {super.key,
      required this.lignes,
      required this.afficherRelais,
      required this.estFaite,
      required this.onToggle,
      required this.estSelectionnee,
      required this.onSelect});

  @override
  Widget build(BuildContext context) {
    debugPrint('LigneTable : ${lignes.length} lignes reçues');
    return Column(children: [
      _entete(),
      Expanded(
        child: ListView.builder(
          itemCount: lignes.length,
          itemBuilder: (context, i) => _ligne(context, lignes[i], i),
        ),
      ),
    ]);
  }

  // --- En-tête : mêmes colonnes que _ligne, mais avec du texte ---
  Widget _entete() {
    const style = TextStyle(fontWeight: FontWeight.bold);

    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10),
      decoration: BoxDecoration(
        border: Border(bottom: BorderSide(color: Colors.grey.shade300)),
      ),
      child: Row(children: [
        const SizedBox(width: _largeurCase), // colonne case à cocher : vide
        const Expanded(
          flex: _flexProprietes,
          child: Center(child: Text('Propriétés', style: style)),
        ),
        if (afficherRelais)
          const Expanded(
            flex: _flexRelais,
            child: Center(child: Text('Relais', style: style)),
          ),
        const Expanded(
          flex: _flexCotation,
          child: Center(child: Text('Cotation', style: style)),
        ),
        const Expanded(
          flex: _flexCouleur,
          child: Center(child: Text('Couleur', style: style)),
        ),
      ]),
    );
  }

  Widget _ligne(BuildContext context, Ligne l, int i) => ListTile(
        selected: estSelectionnee(l.id),
        selectedTileColor:
            Theme.of(context).colorScheme.primary.withValues(alpha: 0.5),
        selectedColor: Theme.of(context).colorScheme.onSurface,
        tileColor: i.isEven ? Colors.grey.shade100 : null,
        onTap: () => onSelect(l.id),
        contentPadding: EdgeInsets.zero,
        minVerticalPadding: 8,
        title: Row(children: [
          SizedBox(
            width: _largeurCase,
            child: Checkbox(
              value: estFaite(l.id),
              onChanged: (_) => onToggle(l.id),
            ),
          ),
          Expanded(
            flex: _flexProprietes,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4),
              child: Wrap(
                alignment: WrapAlignment.center,
                spacing: 4,
                runSpacing: 4,
                children: [
                  for (final propriete in l.proprietes)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.blue,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        propriete,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 11,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                ],
              ),
            ),
          ),
          if (afficherRelais)
            Expanded(
              flex: _flexRelais,
              child: Center(child: Text(l.relais?.toString() ?? '-')),
            ),
          Expanded(
            flex: _flexCotation,
            child: Center(
              // TODO: widget dédié CotationBadge (rond de couleur selon le niveau)
              child: Text(l.cotation),
            ),
          ),
          Expanded(
            flex: _flexCouleur,
            child: Center(
              child: Text(
                l.couleur,
                style: const TextStyle(fontStyle: FontStyle.italic),
              ),
            ),
          ),
        ]),
      );
}

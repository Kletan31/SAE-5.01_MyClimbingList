import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/ligne_model.dart';
import 'package:my_climbing_list_poc/theme/app_theme.dart';

class SelectionVoieBloc extends StatelessWidget {
  final TypeLigne selected;
  final ValueChanged<TypeLigne> onChanged;

  const SelectionVoieBloc({
    super.key,
    required this.selected,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<TypeLigne>(
      showSelectedIcon: false,
      segments: const [
        ButtonSegment(
          value: TypeLigne.voie,
          label: Text('Voie'),
        ),
        ButtonSegment(
          value: TypeLigne.bloc,
          label: Text('Bloc'),
        ),
      ],
      selected: {selected},
      onSelectionChanged: (selection) => onChanged(selection.first),
      style: SegmentedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        selectedForegroundColor: Colors.white,
        selectedBackgroundColor: AppTheme.pageAccent,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }
}

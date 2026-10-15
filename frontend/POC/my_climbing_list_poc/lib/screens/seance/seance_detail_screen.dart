import 'package:flutter/material.dart';
import 'package:my_climbing_list_poc/models/salle_model.dart';
import 'package:my_climbing_list_poc/services/api_service.dart';
import 'package:my_climbing_list_poc/widgets/app_header.dart';
import 'package:provider/provider.dart';

class SeanceDetailScreen extends StatefulWidget {
  final int salleId;
  const SeanceDetailScreen({super.key, required this.salleId});

  @override
  State<SeanceDetailScreen> createState() => _SeanceDetailScreenState();
}

class _SeanceDetailScreenState extends State<SeanceDetailScreen> {
  late final Future<Salle?> _salleFuture;

  @override
  void initState() {
    super.initState();
    _salleFuture = context.read<ApiService>().getSalle(widget.salleId);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Salle?>(
      future: _salleFuture,
      builder: (context, snapshot) {
        final salle = snapshot.data;
        final title = snapshot.connectionState == ConnectionState.waiting
            ? 'Chargement...'
            : snapshot.hasError
                ? 'Erreur'
                : salle?.nom ?? 'Salle inconnue';

        return Scaffold(
          appBar: AppHeader(title: title),
          body: snapshot.connectionState == ConnectionState.waiting
              ? const Center(child: CircularProgressIndicator())
              : snapshot.hasError
                  ? Center(child: Text('Erreur : ${snapshot.error}'))
                  : salle == null
                      ? const Center(child: Text('Salle introuvable'))
                      : Center(
                          child: Text(
                              'Voies disponibles pour la salle ${salle.id}')),
        );
      },
    );
  }
}

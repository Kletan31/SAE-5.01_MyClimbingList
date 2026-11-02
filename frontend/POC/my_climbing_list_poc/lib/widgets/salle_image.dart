import 'package:flutter/material.dart';

class SalleImage extends StatelessWidget {
  const SalleImage({
    super.key,
    required this.reference,
    this.width = 140,
    this.borderRadius = 8,
  });

  static const String _assetsDirectory = 'assets/images/salles/';

  final String reference;
  final double width;
  final double borderRadius;

  @override
  Widget build(BuildContext context) {
    final pixelRatio = MediaQuery.devicePixelRatioOf(context);
    final path = '$_assetsDirectory$reference';

    return SizedBox(
      width: width,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(borderRadius),
        child: Stack(
          children: [
            Positioned.fill(
              child: LayoutBuilder(
                builder: (context, constraints) => Image.asset(
                  path,
                  fit: BoxFit.cover,
                  cacheHeight: (constraints.maxHeight * pixelRatio).round(),
                  errorBuilder: (_, error, __) {
                    debugPrint(
                        'SalleImage : échec du chargement de "$path" -> $error');
                    return const _Placeholder();
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Placeholder extends StatelessWidget {
  const _Placeholder();

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey.shade300,
      child: const Icon(Icons.image_not_supported),
    );
  }
}
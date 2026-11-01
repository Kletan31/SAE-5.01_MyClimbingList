import 'package:flutter/material.dart';


class SalleImage extends StatelessWidget {
  const SalleImage({
    super.key,
    required this.reference,
    this.size = 130,
    this.borderRadius = 8,
  });

  static const String _assetsDirectory = 'assets/images/salles/';

  final String reference;
  final double size;
  final double borderRadius;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: Image.asset(
        '$_assetsDirectory$reference',
        width: size,
        height: size,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) => _Placeholder(size: size),
      ),
    );
  }
}

class _Placeholder extends StatelessWidget {
  const _Placeholder({required this.size});

  final double size;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      color: Colors.grey.shade300,
      child: const Icon(Icons.image_not_supported),
    );
  }
}
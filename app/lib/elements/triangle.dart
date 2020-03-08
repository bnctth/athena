import 'package:athena/constants.dart';
import 'package:flutter/material.dart';

class Triangle extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final path = Path()
      ..lineTo(size.width / 2, size.height)
      ..lineTo(size.width, 0);
    final filled = Paint()
      ..style = PaintingStyle.fill
      ..color = kMainColor;
    canvas.drawShadow(path, Color(0xFF186788), 7, false);
    canvas.drawPath(path, filled);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

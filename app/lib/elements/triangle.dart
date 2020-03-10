import 'dart:io';

import 'package:athena/constants.dart';
import 'package:athena/models/triangle_animation.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TrianglePainting extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final path = Path()
      ..lineTo(0, size.height - kTriangleHeight)
      ..lineTo(size.width / 2, size.height)
      ..lineTo(size.width, size.height - kTriangleHeight)
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

class Triangle extends StatefulWidget {
  @override
  _TriangleState createState() => _TriangleState();
}

class _TriangleState extends State<Triangle>
    with SingleTickerProviderStateMixin {
  AnimationController _controller;
  Animation animation;

  @override
  void initState() {
    _controller = AnimationController(
        vsync: this,
        duration: Duration(milliseconds: 500),
        reverseDuration: Duration(milliseconds: 500));
    _controller.addListener(() {
      setState(() {});
      print(_controller.value);
    });
    animation = Tween(begin: 0.0, end: 800.0).animate(_controller);
    super.initState();
  }

  @override
  void didChangeDependencies() {
    Provider.of<TriangleAnimation>(context).addListener(() {
      if (Provider.of<TriangleAnimation>(context, listen: false).forward)
        _controller.forward();
      else
        _controller.reverse();
    });
    super.didChangeDependencies();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: TrianglePainting(),
      size: Size(
        double.infinity,
        kTriangleHeight + animation.value,
      ),
    );
  }
}

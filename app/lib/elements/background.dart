import 'package:flutter/material.dart';

class Background extends StatelessWidget {
  final Widget child;

  Background({this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: double.infinity,
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: LinearGradient(
            colors: [Color(0xFF3cc4f0), Color(0xFF0a57a1)],
            begin: Alignment.topRight,
            end: Alignment.bottomLeft),
      ),
      child: child,
    );
  }
}

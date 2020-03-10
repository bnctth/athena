import 'package:flutter/foundation.dart';

class TriangleAnimation extends ChangeNotifier {
  bool forward=true;
  void notify(bool f) {
    forward=f;
    notifyListeners();
  }
}

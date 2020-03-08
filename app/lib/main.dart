import 'package:athena/helpers/language_helper.dart';
import 'package:athena/screens/login_screen.dart';
import 'package:flutter/material.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() {
  FlutterError.onError = Crashlytics.instance.recordFlutterError;
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/login',
      routes: <String, Widget Function(BuildContext)>{
        '/login': (context) => LoginScreen(),
      },
    );
  }
}

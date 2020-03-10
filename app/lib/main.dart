import 'package:athena/models/triangle_animation.dart';
import 'package:athena/screens/loading_screen.dart';
import 'package:athena/screens/login_screen.dart';
import 'package:athena/screens/main_screen.dart';
import 'package:flutter/material.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:provider/provider.dart';

void main() {
  FlutterError.onError = Crashlytics.instance.recordFlutterError;
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<TriangleAnimation>(
          create: (_) => TriangleAnimation(),
        ),
      ],
      child: MaterialApp(
        initialRoute: '/loading',
        routes: <String, Widget Function(BuildContext)>{
          '/login': (context) => LoginScreen(),
          '/loading': (context) => LoadingScreen(),
          '/': (context) => MainScreen(),
        },
      ),
    );
  }
}

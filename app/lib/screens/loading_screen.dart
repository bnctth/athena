import 'package:athena/elements/background.dart';
import 'package:athena/helpers/language_helper.dart';
import 'package:athena/helpers/network_helper.dart';
import 'package:flutter/material.dart';

import '../constants.dart';

class LoadingScreen extends StatefulWidget {
  @override
  _LoadingScreenState createState() => _LoadingScreenState();
}

class _LoadingScreenState extends State<LoadingScreen> {
  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    await L.instance.setLang();
    switch (await NetworkHelper.instance.checkStatus) {
      case Status.authenticated:
        Navigator.popAndPushNamed(context, '/');
        break;
      case Status.unknownHost:
      case Status.unauthenticated:
        Navigator.popAndPushNamed(context, '/login');
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Background(
        child: Center(
          child: Text(
            'ATHENA',
            style: TextStyle(
              fontFamily: 'Library 3 am',
              fontSize: 80,
              color: kMainColor,
            ),
          ),
        ),
      ),
    );
  }
}

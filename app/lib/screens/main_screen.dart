import 'package:athena/constants.dart';
import 'package:athena/helpers/network_helper.dart';
import 'package:flutter/material.dart';

class MainScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: RaisedButton(
          color: kMainColor,
          child: Text('logout'),
          onPressed: () {
            NetworkHelper.instance.logout(forgetHost: false);
            Navigator.popAndPushNamed(context, '/login');
          },
        ),
      ),
    );
  }
}

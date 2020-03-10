import 'package:athena/constants.dart';
import 'package:athena/elements/background.dart';
import 'package:athena/elements/triangle.dart';
import 'package:athena/helpers/language_helper.dart';
import 'package:athena/helpers/network_helper.dart';
import 'package:flutter/material.dart';
import 'package:validators/validators.dart';

class LoginScreen extends StatelessWidget {
  String username = '', password = '', host = '';

  @override
  Widget build(BuildContext context) {
    final _formKey = GlobalKey<FormState>();
    return Scaffold(
      body: Background(
        child: Stack(
          children: [
            CustomPaint(
              painter: Triangle(),
              size: Size(double.infinity, 80),
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Form(
                    key: _formKey,
                    child: Column(
                      children: <Widget>[
                        Text(
                          'ATHENA',
                          style: TextStyle(
                            fontFamily: 'Library 3 am',
                            fontSize: 75,
                            color: kMainColor,
                          ),
                        ),
                        SizedBox(
                          height: 75,
                        ),

//                    username
                        TextFormField(
                          decoration:
                              loginTextFieldDecoration(L.map['username']),
                          autocorrect: false,
                          style: kTextFieldStyle,
                          validator: (value) {
                            if (value.isEmpty) {
                              return L.map['nousername'];
                            }
                            return null;
                          },
                          onChanged: (String s) {
                            username = s;
                          },
                        ),
                        SizedBox(
                          height: 20,
                        ),

//                    password
                        TextFormField(
                          decoration:
                              loginTextFieldDecoration(L.map['password']),
                          style: kTextFieldStyle,
                          obscureText: true,
                          validator: (value) {
                            if (value.isEmpty) {
                              return L.map['nopassword'];
                            }
                            return null;
                          },
                          onChanged: (String s) {
                            password = s;
                          },
                        ),
                        SizedBox(
                          height: 20,
                        ),

//                    hostname
                        TextFormField(
                          decoration:
                              loginTextFieldDecoration(L.map['hostname']),
                          style: kTextFieldStyle,
                          keyboardType: TextInputType.url,
                          validator: (value) {
                            if (value.isEmpty) {
                              return L.map['nohostname'];
                            } else if (!isURL(value)) {
                              return L.map['invalidhostname'];
                            }
                            return null;
                          },
                          onChanged: (String s) {
                            host = s;
                          },
                        ),
                        SizedBox(
                          height: 20,
                        ),

//                    submit button
                        RaisedButton(
                          color: kMainColor,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(30.0),
                            side: BorderSide.none,
                          ),
                          onPressed: () async {
                            if (_formKey.currentState.validate()) {
                              if ((await NetworkHelper.instance.login(
                                    username: username,
                                    password: password,
                                    host: host,
                                  )) ==
                                  Status.authenticated) {
                                Navigator.popAndPushNamed(context, '/loading');
                              }
                            }
                          },
                          child: Padding(
                            padding: const EdgeInsets.symmetric(vertical: 10.0),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  L.map['login'],
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                  ),
                                ),
                                Icon(
                                  Icons.arrow_forward,
                                  color: Colors.white,
                                )
                              ],
                            ),
                          ),
                        )
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

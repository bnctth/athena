import 'package:athena/constants.dart';
import 'package:athena/helpers/language_helper.dart';
import 'package:flutter/material.dart';
import 'package:validators/validators.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final _formKey = GlobalKey<FormState>();
    return Scaffold(
      body: Container(
        height: double.infinity,
        width: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [Color(0xFF3cc4f0), Color(0xFF0a57a1)],
              begin: Alignment.topRight,
              end: Alignment.bottomLeft),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
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
                    SizedBox(height: 50,),
                    TextFormField(
                      decoration: loginTextFieldDecoration(L.map['username']),
                      autocorrect: false,
                      validator: (value) {
                        if (value.isEmpty) {
                          return L.map['nousername'];
                        }
                        return null;
                      },
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    TextFormField(
                      decoration: loginTextFieldDecoration(L.map['password']),
                      obscureText: true,
                      validator: (value) {
                        if (value.isEmpty) {
                          return L.map['nopassword'];
                        }
                        return null;
                      },
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    TextFormField(
                      decoration: loginTextFieldDecoration(L.map['hostname']),
                      keyboardType: TextInputType.url,
                      validator: (value) {
                        if (value.isEmpty) {
                          return L.map['nohostname'];
                        } else if (!isURL(value)) {
                          return L.map['invalidhostname'];
                        }
                        return null;
                      },
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    RaisedButton(
                      color: kMainColor,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30.0),
                        side: BorderSide.none,
                      ),
                      onPressed: () {
                        print(_formKey.currentState.validate());
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
      ),
    );
  }
}

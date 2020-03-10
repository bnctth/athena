import 'dart:io';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum Language { Hungarian, English }

class L {
  Language lang;
  static final L instance = L._private();

  factory L() => instance;

  L._private();

  Future<void> setLang() async {
    switch ((await SharedPreferences.getInstance()).getString('language') ??
        'eng') {
//      TODO get device language
      case 'hun':
        lang = Language.Hungarian;
        break;
      case 'eng':
        lang = Language.English;
        break;
    }
  }

  static const English = {
    'username': 'Username',
    'nousername': 'Please enter your username',
    'password': 'Password',
    'nopassword': 'Please enter your password',
    'hostname': 'Hostname',
    'nohostname': 'Please enter the hostname of your hub',
    'invalidhostname': 'Please enter a valid hostname',
    'login': 'Log in',
    'unknownhost':
        'At this minute connecting to the given hostname was not possible',
  };
  static const Hungarian = {
    'username': 'Felhasználónév',
    'nousername': 'Kérlek, add meg a felhasználóneved',
    'password': 'Jelszó',
    'nopassword': 'Kérlek, add meg a jelszavadat',
    'hostname': 'Webcím',
    'nohostname': 'Kérlek, add meg a hub eszközöd webcímét',
    'invalidhostname': 'Kérlek egy valós webcímet adj meg',
    'login': 'Bejelentkezés',
    'unknownhost': 'Jelen pillanatban a megadott webcím nem elérhető'
  };

  static Map<String, String> get map {
    switch (instance.lang) {
      case Language.English:
        return English;
        break;
      case Language.Hungarian:
        return Hungarian;
        break;
//      ************************************************************************
      default:
        return English;
//        ************************************************************************
    }
    return null;
  }
}

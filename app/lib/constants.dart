import 'package:flutter/material.dart';

InputDecoration loginTextFieldDecoration(String hintText) => InputDecoration(
      hintText: hintText,
      hintStyle: TextStyle(color: Colors.white),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30),
        borderSide: BorderSide(
          color: Colors.white,
          width: 3,
        ),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30),
        borderSide: BorderSide(
          color: Colors.white,
          width: 3,
        ),
      ),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30),
        borderSide: BorderSide(
          color: Colors.white,
          width: 3,
        ),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30),
        borderSide: BorderSide(
          color: Colors.red,
          width: 3,
        ),
      ),
      contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 0),
      errorStyle: TextStyle(fontSize: 15),
    );

const kMainColor=Color(0xFFf6d309);
import 'dart:convert';
import 'dart:io';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

enum Status { authenticated, unauthenticated }
enum Method { get, post }

class NetworkHelper {
  static final NetworkHelper instance = NetworkHelper._private();

  NetworkHelper._private();

  String _at, _rt, _host;

  DateTime renewNeededAt = DateTime.now();
  final ss = new FlutterSecureStorage();

  factory NetworkHelper() => instance;

//  check if saved tokens exists and tries to renew
  Future<Status> get checkStatus async {
    _at = await ss.read(key: 'access_token');
    _rt = await ss.read(key: 'refresh_token');
    _host = (await SharedPreferences.getInstance()).getString('host');
    if (_at == null || _rt == null || _host == null)
      return Status.unauthenticated;
    if (await _renew()) return Status.authenticated;
    return Status.unauthenticated;
  }

//  renew the tokens and returns if succeeded
  Future<bool> _renew() async {
    http.Response response = await _request('/auth/renew', Method.post,
        body: {'refresh_token': _rt}, isAuthenticated: false);
    if (response.statusCode == 200) {
      _at = jsonDecode(response.body)['access_token'];
      _rt = jsonDecode(response.body)['refresh_token'];
      ss.write(key: 'access_token', value: _at);
      ss.write(key: 'refresh_token', value: _rt);
      renewNeededAt = DateTime.now()
          .add(Duration(seconds: jsonDecode(response.body)['expires_in']));
      return true;
    }
    return false;
  }

  Future<Status> login({String username, String password, String host}) async {
    if (host.substring(0, 3) != 'http') host = 'http://$host';
    _host = host;
    (await SharedPreferences.getInstance()).setString('host', _host);
    http.Response response = await _request('/auth/login', Method.post,
        body: {'username': username, 'password': password},
        isAuthenticated: false);
    if (response.statusCode == 200) {
      Map<String, dynamic> decoded = jsonDecode(response.body);
      _at = decoded['access_token'];
      _rt = decoded['refresh_token'];
      ss.write(key: 'access_token', value: _at);
      ss.write(key: 'refresh_token', value: _rt);
      return Status.authenticated;
    }
    return Status.unauthenticated;
  }

  Future<http.Response> _request(String path, Method method,
      {Map<String, dynamic> body = const {},
      bool isAuthenticated = true}) async {
    http.Response response;
    if (isAuthenticated && renewNeededAt.isBefore(DateTime.now())) _renew();
    try {
      if (method == Method.get) {
        response = await http.get(
          '$_host$path',
          headers: isAuthenticated ? {'Authorization': 'Bearer $_at'} : null,
        );
      } else {
        response = await http.post(
          '$_host$path',
          body: body,
          headers: isAuthenticated ? {'Authorization': 'Bearer $_at'} : null,
        );
      }
    } catch (e) {
      if (e.runtimeType == SocketException) {
        print("wrong host: $_host$path");
//        TODO implement wrong host
        return http.Response('', 410);
      } else {
        throw (e);
      }
    }
    return response;
  }
}

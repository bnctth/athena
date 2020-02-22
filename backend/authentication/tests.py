from datetime import timedelta

import freezegun
from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.utils import timezone


class AuthTests(TestCase):
    loginPath = '/auth/login'
    renewPath = '/auth/renew'
    testPath = '/auth/loginrequiredtest'

    def setUp(self):
        User.objects.create_user('test', password='test')

    def test_login(self):
        c = Client()

        # test wrong method
        response = c.get(self.loginPath)
        self.assertEqual(response.status_code, 405)

        # test wrong credentials
        response = c.post(self.loginPath, {'username': 'foo', 'password': 'bar'})
        self.assertEqual(response.status_code, 401)

        # test good credentials
        response = c.post(self.loginPath, {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        at = response.json()['access_token']

        # test tokens
        ac = Client(HTTP_AUTHORIZATION=f'Bearer {at}')
        response = ac.get(self.testPath)
        self.assertEqual(response.status_code, 200)

        # test token expiration
        with freezegun.freeze_time(timezone.now() + timedelta(hours=2)):
            response = ac.get(self.testPath)
            self.assertEqual(response.status_code, 401)

    def test_renew(self):
        c = Client()

        # get tokens
        response = c.post('/auth/login', {'username': 'test', 'password': 'test'})
        oldat = response.json()['access_token']
        oldrt = response.json()['refresh_token']

        # test wrong method
        response = c.get(self.renewPath)
        self.assertEqual(response.status_code, 405)

        # test wrong refresh token
        response = c.post(self.renewPath, {'refresh_token': 'a.a.a'})
        self.assertEqual(response.status_code, 401)

        # test correct refresh token
        response = c.post(self.renewPath, {'refresh_token': oldrt})
        self.assertEqual(response.status_code, 200)
        at = response.json()['access_token']
        rt = response.json()['refresh_token']

        # test invalidating
        response = c.get(self.testPath, **{'HTTP_AUTHORIZATION': f'Bearer {oldat}'})
        self.assertEqual(response.status_code, 401)
        response = c.post(self.renewPath, {'refresh_token': oldrt})
        self.assertEqual(response.status_code, 401)

        # test new tokens
        response = c.get(self.testPath, **{'HTTP_AUTHORIZATION': f'Bearer {at}'})
        self.assertEqual(response.status_code, 200)
        response = c.post(self.renewPath, {'refresh_token': rt})
        self.assertEqual(response.status_code, 200)

        # test expiration
        with freezegun.freeze_time(timezone.now() + timedelta(days=65)):
            response = c.post(self.renewPath, {'refresh_token': rt})
            self.assertEqual(response.status_code, 401)

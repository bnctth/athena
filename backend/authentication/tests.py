from django.contrib.auth.models import User
from django.test import TestCase, Client


# Create your tests here.
class AuthTests(TestCase):
    def setUp(self):
        User.objects.create_user('test', password='test')

    def test_login(self):
        c = Client()
        response = c.get('/auth/login')
        self.assertEqual(response.status_code, 405)
        response = c.post('/auth/login', {'username': 'foo', 'password': 'bar'})
        self.assertEqual(response.status_code, 401)
        response = c.post('/auth/login', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.at = response.json()['access_token']
        response = c.get('/auth/loginrequiredtest', **{'HTTP_AUTHORIZATION': f'Bearer {self.at}'})
        self.assertEqual(response.status_code, 200)

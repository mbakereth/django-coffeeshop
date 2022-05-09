from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.urls import resolve
from .views import *

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.testuser = User.objects.create_user(
            username='testuser',
            email='testuser@myapp.com',
            password='testpass123')
    def test_authorized(self):
        url = '/basket/'
        request = self.factory.get(url)
        myview, myargs, mykwargs = resolve(url)
        request.user = self.testuser
        response = myview(request)
        self.assertEqual(response.status_code, 200)
    def test_unauthorized(self):
        url = '/basket/'
        request = self.factory.get(url)
        myview, myargs, mykwargs = resolve(url)
        request.user = AnonymousUser()
        response = myview(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/account/login/?next=/basket/')


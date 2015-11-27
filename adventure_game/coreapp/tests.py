import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User

from coreapp.views import auth_view
from coreapp.views import registration_submission
from coreapp.views import add_family_member_submission

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser',password='testpass', last_name="test")

    def test_auth_view_invalid_user(self):
        response = self.client.post('/auth/',{'username': 'sam123', 'password': 'abc123'},follow=True)
        self.assertRedirects(response,'/')
        message = list(response.context['messages'])
        self.assertEqual("The account you entered is invalid, please try again!", str(message[0]))


    def test_auth_view_valid_user(self):
        response = self.client.post('/auth/',{'username':'testuser','password':'testpass'},follow=True)
        self.assertRedirects(response,'/')
        message = list(response.context['messages'])
        self.assertEqual("Hi test, you have successfully logged in." , str(message[0]))


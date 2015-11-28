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

    def test_auth_view_redirect(self):
        response = self.client.post('/auth/',{'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code,302)

    def test_auth_view_invalid_user(self):
        response = self.client.post('/auth/',{'username': 'sam123', 'password': 'abc123'},follow=True)
        message = list(response.context['messages'])
        self.assertEqual("The account you entered is invalid, please try again!", str(message[0]))


    def test_auth_view_valid_user(self):
        response = self.client.post('/auth/',{'username':'testuser','password':'testpass'},follow=True)
        self.assertRedirects(response,'/')
        message = list(response.context['messages'])
        self.assertEqual("Hi test, you have successfully logged in." , str(message[0]))


class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser',password='pass',email = "test@123.com")

    def test_register_redirect(self):
        response = self.client.post("/registration-submission/",{'username' : 'test', 'password': 'test', 'email' : 'test123@123.com'})
        self.assertEqual(response.status_code,302)

    def test_duplicate_user(self):
        response = self.client.post("/registration-submission/",{'username': 'testuser'})
        self.assertEqual(response.context['message'],"Try again, the username testuser is already taken.")

    def test_duplicate_email(self):
        response = self.client.post("/registration-submission/",{'email': 'test@123.com'})
        self.assertEqual(response.context['message'],"Try again, there is already an account with that email test@123.com.")

    def test_register_success_auto_login(self):
        response = self.client.post("/registration-submission/",{'username' : 'test', 'password': 'test', 'email' : 'test123@123.com'},follow=True)
        self.assertIn('_auth_user_id',self.client.session)

class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()


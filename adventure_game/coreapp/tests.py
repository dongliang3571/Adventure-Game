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
        self.user = User.objects.create_user(username='testuser',password='pass')

    def test_view_not_loggedin(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code,302)

    def test_context(self):
        self.assertTrue(self.client.login(username='testuser',password='pass'))
        self.user.character_set.create(character_name="testchar",character_pin="1234")
        self.assertEqual(len(self.user.character_set.all()),1)
        response = self.client.get('/profile/')
        family_members = list(response.context['family_members'])
        self.assertEqual(str(family_members[0]),'testchar')

class AddFamilyMemberTests(TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username='testuser',password='pass')
        self.client.login(username='testuser',password='pass')

    def test_pin_invalid_length(self):
        response = self.client.post('/add-family-member-submission/',{'member-name':'test','member-pin' :'12345'},follow=True)
        self.assertRedirects(response,'/add-family-member/')
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]),'Please enter 4 characters as your PIN number')

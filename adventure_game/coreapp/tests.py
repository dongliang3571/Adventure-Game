import unittest
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from coreapp.views import auth_view
from coreapp.views import registration_submission

class AccountTests(TestCase):

    #login test with unregistred user
    def test_login_redirect(self):
        c=Client()

        #Supposed to fail. User is not registered - should give redirect code 302
        response = c.post('/auth/',{'username': 'sam123', 'password': 'abc123'})
        self.assertRedirects(response,'invalid_login')

    #register user then login
    def test_regi_and_login(self):
        c2=Client()

        regi_response = c2.post('registrationSubmission',{'username':'janice22','firstname':'janice','lastname':'goralnik', 'email':'friends@show.com','password':'yemen'})
        self.assertEqual(regi_response.status_code,200)

        login_response = c2.post('/auth/',{'username':'janice22','password':'yemen'})
        self.assertEqual(login_response.status_code,200)

class SimpleTest(TestCase):
    def test_add(self):
        self.assertEqual(1+1,2)

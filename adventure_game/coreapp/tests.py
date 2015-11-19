import unittest
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from coreapp.views import auth_view
from coreapp.views import registration_submission
from coreapp.views import add_family_member_submission

class AccountTests(TestCase):

    #login test with unregistred user
    def test_login_fail(self):
        c = Client()
        #Supposed to fail. User is not registered - should give redirect code 302
        response = c.post('/auth/', {'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code, 302)

    #register user
    def test_regi(self):
        c2 = Client()
        regi_response = c2.post('/registration-submission/', {'username':'janice22', 'firstname':'janice', 'lastname':'goralnik', 'email':'friends@show.com', 'password':'yemen'})
        self.assertEqual(regi_response.status_code, 302)

    #login test that's supposed to pass
    def test_login_pass(self):
        c3 = Client()
        login_response = c3.post('/auth/', {'username':'janice22', 'password':'yemen'})
        self.assertEqual(login_response.status_code, 302)

    #create new family member
    def test_create_family_member(self):
        c4 = Client()
        member_response = c4.post('/add-family-member-submission/', {'member-name':'Mom', 'member-pin':'1221'})
        self.assertEqual(member_response.status_code, 302)

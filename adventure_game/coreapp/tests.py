import unittest
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from coreapp.views import auth_view

class AccountTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.c = User.objects.create_user(username="sam123", email="test@test.com", password="abc123")
    #login test
    def test_login(self):
        response = self.c.login('/auth/',{'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code,200)

class SimpleTest(TestCase):
    def test_add(self):
        self.assertEqual(1+1,2)

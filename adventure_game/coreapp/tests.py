import unittest
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from coreapp.views import auth_view

class AccountTests(TestCase):

    #login test
    def test_login(self):
        c=Client()
        response = c.post('/auth/',{'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code,200)

class SimpleTest(TestCase):
    def test_add(self):
        self.assertEqual(1+1,2)

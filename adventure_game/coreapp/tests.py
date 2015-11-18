import unittest
from django.test import TestCase
from django.test import Client

class AccountTests(TestCase):

    def setUp(self):
        self.user = Client()
    #registration test
    def test_regi(self):
        info = self.user.post('/registration-submission/',{'username': 'sam123', 'email': 'abc@gmail.com', 'password': 'abc123'})
        self.assertEqual(info.status_code,200)

    #login test
    def test_login(self):
        response = self.user.post('/auth/',{'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code,200)

class SimpleTest(TestCase):
    def test_add(self):
        self.assertEqual(1+1,2)

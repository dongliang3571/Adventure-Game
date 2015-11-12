import unittest
from django.test import TestCase
from django.test import Client

class AccountTests(unittest.TestCase):

    def setUp(self):
        self.user = Client()
    #registration test
    def regi_test(self):
        info = self.user.post('/registration/',{'username': 'sam123', 'email': 'abc@gmail.com', 'password': 'abc123'})
        self.assertEqual(info.status_code,200)

    #login test
    def login_test(self):
        response = self.user.post('/login/',{'username': 'jennifer', 'password': 'secret'})
        self.assertEqual(response.status_code,200)

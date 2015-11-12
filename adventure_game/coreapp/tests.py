from django.test import TestCase
from django.test import Client

#login test
def login_test(self):
    c = Client()
    response = c.post('/login/',{'username': 'jennifer', 'password': 'secret'})
    self.assertEqual(response.status_code,200)

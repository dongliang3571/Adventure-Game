from django.test import TestCase
from django.test import Client

#login test
def login_test(self):
    user = Client()
    response = user.post('/login/',{'username': 'jennifer', 'password': 'secret'})
    self.assertEqual(response.status_code,200)

#registration test
def regi_test(self):
    new_user = Client()
    info = new_user.post('/registration/',{'username': 'sam123', 'email': 'abc@gmail.com', 'password': 'abc123'})
    self.assertEqual(info.status_code,200)

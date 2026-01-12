#from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

class RegisterTestCase(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))  # 'register' is URL name
        self.assertEqual(response.status_code, 200)

    def test_register_form_submission(self):
        response = self.client.post(reverse('register'), {
            'name': 'Ravi',
            'email': 'ravi@example.com',
            'contactno': '9876543210',
            'password': 'pass123',
            'cpassword': 'pass123'
        })
        # Change the expected status_code as per your view logic
        self.assertEqual(response.status_code, 302)  # assuming it redirects after success
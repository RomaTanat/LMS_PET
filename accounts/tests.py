from django.test import TestCase, Client
from django.urls import reverse

class LoginViewTest(TestCase):
    def test_login_view(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

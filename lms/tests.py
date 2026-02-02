from django.test import TestCase, Client
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

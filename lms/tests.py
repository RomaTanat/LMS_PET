from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()

class ChatTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client = Client()
        self.client.login(username='user1', password='password')

    def test_chat_index(self):
        # Requires 'chat:index' to exist
        url = reverse('chat:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')
        # Check if user2 is in the list (context['all_users'])
        self.assertContains(response, 'user2')

    def test_start_private_chat(self):
        url = reverse('chat:start_private_chat', args=['user2'])
        response = self.client.get(url)
        # Should redirect to /chat/user1_user2/
        target_room = 'user1_user2'
        # Note: sorted(['user1', 'user2']) is ['user1', 'user2']
        expected_url = reverse('chat:room', args=[target_room])
        self.assertRedirects(response, expected_url)

class ErrorPageTests(TestCase):
    def test_404_template(self):
        try:
            content = render_to_string('404.html')
            self.assertIn('404', content)
            self.assertIn('glass-panel', content)
        except Exception as e:
            self.fail(f"404 template failed to render: {e}")

    def test_403_template(self):
        try:
            content = render_to_string('403.html')
            self.assertIn('403', content)
        except Exception as e:
            self.fail(f"403 template failed to render: {e}")

    def test_500_template(self):
        try:
            content = render_to_string('500.html')
            self.assertIn('500', content)
        except Exception as e:
            self.fail(f"500 template failed to render: {e}")

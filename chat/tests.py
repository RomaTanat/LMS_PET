from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class ChatTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')

    def test_start_private_chat_redirect(self):
        other_user = get_user_model().objects.create_user(username='otheruser', password='password')
        response = self.client.get(reverse('chat:start_private_chat', kwargs={'target_username': 'otheruser'}))

        # Expected room name: otheruser_testuser (sorted)
        expected_room = 'otheruser_testuser'
        expected_url = reverse('chat:room', kwargs={'room_name': expected_room})

        self.assertRedirects(response, expected_url)

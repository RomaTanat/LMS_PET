from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.force_login(self.user)

    def test_chat_index(self):
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')

    def test_start_private_chat(self):
        other_user = User.objects.create_user(username='other', password='password')
        url = reverse('chat:start_private_chat', args=[other_user.username])
        response = self.client.get(url)
        # Should redirect to the room
        self.assertEqual(response.status_code, 302)
        # Room name should be sorted usernames
        expected_room = 'other_testuser' # 'o' comes before 't'
        self.assertIn(expected_room, response.url)


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from chat.models import Room

User = get_user_model()

class ChatViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client = Client()
        self.client.login(username='user1', password='password')

    def test_start_private_chat_creates_room_and_redirects(self):
        url = reverse('chat:start_private_chat', args=['user2'])
        response = self.client.get(url)

        # Check redirection
        expected_room_name = 'user1_user2'
        room_url = reverse('chat:room', kwargs={'room_name': expected_room_name})
        self.assertRedirects(response, room_url)

        # Check room creation
        room = Room.objects.get(name=expected_room_name)
        self.assertEqual(room.slug, expected_room_name)

    def test_rooms_view(self):
        url = reverse('chat:rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')
        self.assertIn(self.user2, response.context['all_users'])
        self.assertNotIn(self.user1, response.context['all_users'])

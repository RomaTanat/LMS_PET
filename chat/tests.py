from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Room, Message

User = get_user_model()

class ChatViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = Client()
        self.client.login(username='user1', password='password123')

    def test_rooms_view(self):
        url = reverse('chat:rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')
        self.assertIn('all_users', response.context)
        # Verify user2 is in the list
        self.assertIn(self.user2, response.context['all_users'])
        # Verify user1 is NOT in the list (exclude self)
        self.assertNotIn(self.user1, response.context['all_users'])

    def test_start_private_chat(self):
        # target user is user2
        url = reverse('chat:start_private_chat', args=['user2'])
        response = self.client.get(url)

        # Should redirect to the room
        # Room name should be user1_user2 (sorted)
        expected_room_name = 'user1_user2'
        expected_url = reverse('chat:room', args=[expected_room_name])

        self.assertRedirects(response, expected_url)

    def test_room_view_creation(self):
        room_name = 'test_room'
        url = reverse('chat:room', args=[room_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')

        # Verify room was created
        self.assertTrue(Room.objects.filter(name=room_name).exists())

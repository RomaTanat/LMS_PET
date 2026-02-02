from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Room, Message

User = get_user_model()

class ChatTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client.force_login(self.user1)

    def test_index_view(self):
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')
        self.assertContains(response, 'user2')
        # Check if AI_Tutor is created
        self.assertTrue(User.objects.filter(username='AI_Tutor').exists())

    def test_start_private_chat_ai(self):
        User.objects.create_user(username='AI_Tutor')
        response = self.client.get(reverse('chat:start_private_chat', kwargs={'target_username': 'AI_Tutor'}))
        expected_url = reverse('chat:room', kwargs={'room_name': f'mentor_{self.user1.username}'})
        self.assertRedirects(response, expected_url)

    def test_start_private_chat_user(self):
        response = self.client.get(reverse('chat:start_private_chat', kwargs={'target_username': 'user2'}))
        # Sorted usernames: user1, user2 -> user1_user2
        expected_room = 'user1_user2'
        expected_url = reverse('chat:room', kwargs={'room_name': expected_room})
        self.assertRedirects(response, expected_url)

    def test_room_view(self):
        response = self.client.get(reverse('chat:room', kwargs={'room_name': 'test_room'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertTrue(Room.objects.filter(name='test_room').exists())

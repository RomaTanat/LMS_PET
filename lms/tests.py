from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from lms.models import Course

User = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user2 = User.objects.create_user(username='otheruser', password='password')
        self.course = Course.objects.create(title='Test Course', description='Desc', author=self.user)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 1)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_redirect(self):
        self.client.force_login(self.user)
        # accounts/urls.py defines 'profile'
        url = reverse('profile')

        response = self.client.get(url)
        # Should redirect to user_profile (lms view)
        self.assertRedirects(response, reverse('user_profile'))

    def test_chat_lobby(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/rooms.html')
        self.assertIn('all_users', response.context)
        # Should exclude self
        self.assertEqual(len(response.context['all_users']), 1) # only otheruser
        self.assertEqual(response.context['all_users'][0], self.user2)

    def test_start_private_chat(self):
        self.client.force_login(self.user)
        url = reverse('chat:start_private_chat', kwargs={'target_username': 'otheruser'})
        response = self.client.get(url)
        # Room name: otheruser_testuser (sorted o, t)
        expected_room = 'otheruser_testuser'
        self.assertRedirects(response, reverse('chat:room', kwargs={'room_name': expected_room}))

    @override_settings(DEBUG=False)
    def test_404(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

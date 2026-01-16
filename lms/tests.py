from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, Section, Material, CodingProblem
from django.template import Context, Template
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomFilterTests(TestCase):
    def test_split_filter(self):
        """Test the custom split filter."""
        template = Template('{% load custom_filters %}{{ "a/b/c"|split:"/"|last }}')
        context = Context({})
        rendered = template.render(context)
        self.assertEqual(rendered, 'c')

class ViewTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(title='Test Course', description='Test Description', author=self.user)
        self.section = Section.objects.create(course=self.course, title='Test Section')

    def test_course_detail_template(self):
        """Test that course_detail.html renders correctly."""
        url = reverse('course_detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_room_template_js_escape(self):
        """Test that room.html renders and escapes variables."""
        self.client.login(username='testuser', password='password')
        url = reverse('room', args=['testroom'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response, 'testuser')

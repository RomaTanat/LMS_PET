from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .models import Course, Section, Material, ContentBlock, CodingProblem

class ErrorPageTests(TestCase):
    @override_settings(DEBUG=False)
    def test_404_page(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

class CourseDetailTests(TestCase):
    def setUp(self):
        # Create user (author)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.user = User.objects.create_user(username='author', password='password')

        self.course = Course.objects.create(title='Test Course', author=self.user)
        self.section = Section.objects.create(course=self.course, title='Test Section')
        self.material = Material.objects.create(section=self.section, title='Test Material')
        # Create a coding problem
        self.coding_problem = CodingProblem.objects.create(
            title="Test Problem",
            description="Solve this",
            input_data="1",
            expected_output="2",
            material=self.material
        )

    def test_course_detail_renders(self):
        url = reverse('course_detail', args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, 'Test Problem')

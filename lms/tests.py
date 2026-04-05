from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, Section, Material, CodingProblem, User

class LMSViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(title="Test Course", description="Test Description", author=self.user)
        self.section = Section.objects.create(course=self.course, title="Test Section", order=1)
        self.material = Material.objects.create(section=self.section, title="Test Material", order=1)
        self.problem = CodingProblem.objects.create(
            title="Test Problem",
            description="Test Description",
            input_data="1",
            expected_output="1",
            material=self.material
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('courses', response.context)
        self.assertContains(response, "Test Course")

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Problem")

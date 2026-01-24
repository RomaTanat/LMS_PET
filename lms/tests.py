from django.test import TestCase, override_settings

class ErrorPageTests(TestCase):
    @override_settings(DEBUG=False)
    def test_404_page(self):
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, 'glass-panel', status_code=404)

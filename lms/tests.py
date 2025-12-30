from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import CodingProblem, Submission, Material, Course, Section, Achievement
from django.contrib.auth import get_user_model
from .services import analyze_code_submission
import json

User = get_user_model()

class AnalyzeCodeSubmissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(title="Test Course", author=self.user)
        self.section = Section.objects.create(course=self.course, title="Test Section")
        self.material = Material.objects.create(section=self.section, title="Test Material")

        self.problem = CodingProblem.objects.create(
            title="Sum two numbers",
            description="Write a function that adds two numbers",
            input_data="1 2",
            expected_output="3",
            material=self.material,
            test_cases=[
                {"stdin": "1\n2", "stdout": "3", "is_hidden": False, "timeout": 1},
                {"stdin": "10\n20", "stdout": "30", "is_hidden": True, "timeout": 1}
            ],
            reference_solution="print(int(input()) + int(input()))"
        )

    def test_submission_accepted(self):
        code = "a = int(input())\nb = int(input())\nprint(a + b)"
        submission = Submission.objects.create(
            problem=self.problem,
            student=self.user,
            code=code
        )

        processed_submission = analyze_code_submission(submission)

        self.assertEqual(processed_submission.status, 'ACCEPTED')
        feedback = json.loads(processed_submission.feedback)
        self.assertIn("warm_hint", feedback)
        self.assertIn("Все тесты пройдены", feedback["warm_hint"])

    @patch('lms.services.get_ai_feedback')
    def test_submission_failed_ai_called(self, mock_get_ai_feedback):
        # Mocking AI response
        mock_response = {
            "warm_hint": "Try checking your addition logic.",
            "alert_error": "Wrong answer on test case 1."
        }
        mock_get_ai_feedback.return_value = mock_response

        # Wrong code
        code = "print(0)"
        submission = Submission.objects.create(
            problem=self.problem,
            student=self.user,
            code=code
        )

        processed_submission = analyze_code_submission(submission)

        self.assertEqual(processed_submission.status, 'FAILED')
        feedback = json.loads(processed_submission.feedback)
        self.assertEqual(feedback['warm_hint'], mock_response['warm_hint'])
        self.assertEqual(feedback['alert_error'], mock_response['alert_error'])

        # Verify AI service was called with correct arguments
        mock_get_ai_feedback.assert_called_once()
        args, _ = mock_get_ai_feedback.call_args
        self.assertEqual(args[0], code) # Passed code
        # args[1] is failure_reason, which is a dict, we can check basic properties
        self.assertEqual(args[1]['status'], 'WRONG_ANSWER')
        self.assertEqual(args[2], self.problem.reference_solution)

    @patch('openai.OpenAI')
    def test_real_ai_integration_mock(self, mock_openai):
        # Test the actual get_ai_feedback function logic with mocked OpenAI client
        from lms.services import get_ai_feedback

        # Mock the client instance and its response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = json.dumps({
            "warm_hint": "Mock Hint",
            "alert_error": "Mock Error"
        })
        mock_client.chat.completions.create.return_value = mock_completion

        result = get_ai_feedback("code", {"status": "ERROR"}, "reference")

        self.assertEqual(result['warm_hint'], "Mock Hint")
        self.assertEqual(result['alert_error'], "Mock Error")

        # Verify prompt construction (implied by call)
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['response_format'], {"type": "json_object"})
        messages = call_kwargs['messages']
        self.assertIn("Эталонное решение", messages[0]['content'])


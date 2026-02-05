import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lms_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'password123')
    print("Created testuser")

if not User.objects.filter(username='otheruser').exists():
    User.objects.create_user('otheruser', 'other@example.com', 'password123')
    print("Created otheruser")

if not User.objects.filter(username='AI_Tutor').exists():
    User.objects.create_user('AI_Tutor', 'ai@example.com', 'password123')
    print("Created AI_Tutor")

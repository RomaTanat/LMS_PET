import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lms_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from lms.models import StudentProfile

User = get_user_model()

# Create users
for i in range(1, 6):
    username = f'user{i}'
    email = f'user{i}@example.com'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password='password123')
        # Profile should be created by signal, but let's make sure and add XP
        # Reload user to access related profile if signal worked
        user.refresh_from_db()

        if hasattr(user, 'student_profile'):
            profile = user.student_profile
            profile.total_xp = i * 100
            profile.level = i
            profile.save()
            print(f"Created {username} with {profile.total_xp} XP")
        else:
             print(f"Profile not found for {username}")
    else:
        print(f"User {username} already exists")

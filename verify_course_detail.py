import os
import django
from playwright.sync_api import sync_playwright

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lms_project.settings')
django.setup()
from lms.models import Course

course = Course.objects.get(title="Python Verification Course")
course_url = f"http://127.0.0.1:8000/courses/{course.id}/"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Login
        page.goto("http://127.0.0.1:8000/accounts/login/")
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "password")
        page.click("button[type='submit']")
        # Wait for redirect, flexible in case of profile or home
        page.wait_for_load_state("networkidle")

        # Go to course detail
        print(f"Navigating to {course_url}")
        page.goto(course_url)
        page.wait_for_selector("h1") # Wait for title

        page.screenshot(path="/home/jules/verification/course_detail_before_fix.png", full_page=True)

        content = page.content()
        # "Практика кода" is the header for the section
        if "Практика кода" in content:
            print("Coding Problem Section FOUND")
        else:
            print("Coding Problem Section NOT FOUND")

        if "Verify Print" in content:
             print("Problem Title FOUND")
        else:
             print("Problem Title NOT FOUND")

        browser.close()

if __name__ == "__main__":
    run()

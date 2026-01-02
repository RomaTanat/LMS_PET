from playwright.sync_api import sync_playwright
import os
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            # Login
            print("Navigating to login...")
            page.goto("http://localhost:8000/accounts/login/")
            page.fill("input[name='username']", "testuser")
            page.fill("input[name='password']", "password")
            print("Submitting login form...")
            page.get_by_role("button", name="Войти").click()

            print("Waiting for navigation...")
            page.wait_for_load_state("networkidle")

            print(f"Current URL: {page.url}")
            print(f"Page title: {page.title()}")

            # Navigate to Chat
            print("Looking for Chat link...")
            # Try to find the link by partial text or href
            chat_link = page.get_by_role("link", name="Чат")
            if chat_link.count() > 0:
                print("Clicking Chat link...")
                chat_link.click()
            else:
                print("Chat link not found via role. Trying explicit text...")
                page.click("text=💬 Чат")

            # Verify and screenshot
            print("Waiting for contact list...")
            page.wait_for_selector("text=Список контактов")

            # Ensure directory exists
            os.makedirs("verification", exist_ok=True)

            page.screenshot(path="verification/chat_rooms.png")
            print("Screenshot saved to verification/chat_rooms.png")

        except Exception as e:
            print(f"Error: {e}")
            os.makedirs("verification", exist_ok=True)
            page.screenshot(path="verification/error.png")
            print("Error screenshot saved to verification/error.png")
            print(page.content())

        finally:
            browser.close()

if __name__ == "__main__":
    run()
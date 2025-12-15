import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_profile_update_and_password_change(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Register a new user
        page.goto(f"{live_server}/register")
        page.fill('input[name="first_name"]', "E2E")
        page.fill('input[name="last_name"]', "User")
        page.fill('input[name="email"]', "e2euser@example.com")
        page.fill('input[name="username"]', "e2euser")
        page.fill('input[name="password"]', "E2Epass123!")
        page.fill('input[name="confirm_password"]', "E2Epass123!")
        page.click('button[type="submit"]')
        # Login
        page.goto(f"{live_server}/login")
        page.fill('input[name="username"]', "e2euser")
        page.fill('input[name="password"]', "E2Epass123!")
        page.click('button[type="submit"]')
        # Go to profile page
        page.goto(f"{live_server}/profile")
        # Update profile
        page.fill('input[name="first_name"]', "E2E2")
        page.click('#profile-form button[type="submit"]')
        page.wait_for_selector('#profile-message')
        assert "Profile updated" in page.inner_text('#profile-message')
        # Change password
        page.fill('input[name="current_password"]', "E2Epass123!")
        page.fill('input[name="new_password"]', "E2Epass456!")
        page.fill('input[name="confirm_new_password"]', "E2Epass456!")
        page.click('#password-form button[type="submit"]')
        page.wait_for_selector('#password-message')
        assert "Password changed" in page.inner_text('#password-message')
        # Logout (simulate by clearing localStorage)
        page.evaluate("localStorage.clear()")
        # Try to login with new password
        page.goto(f"{live_server}/login")
        page.fill('input[name="username"]', "e2euser")
        page.fill('input[name="password"]', "E2Epass456!")
        page.click('button[type="submit"]')
        # Should be redirected to dashboard or see dashboard content
        assert page.url.endswith("/dashboard")
        browser.close()

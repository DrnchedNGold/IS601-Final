import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_profile_update_and_password_change_flow(page: Page, fastapi_server):
    """E2E test for complete user profile and password change workflow"""
    
    # Navigate to registration page
    page.goto(f"{fastapi_server}register")
    
    # Register a new user
    page.fill('input[name="username"]', "profileuser")
    page.fill('input[name="email"]', "profile@example.com")
    page.fill('input[name="first_name"]', "Profile")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    
    page.click('button[type="submit"]')
    
    # Wait for success message and redirect
    page.wait_for_url("**/login", timeout=10000)
    
    # Login with the new user
    page.fill('input[name="username"]', "profileuser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    # Wait for dashboard
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Navigate to profile page
    page.goto(f"{fastapi_server}profile")
    
    # Verify profile data is loaded
    expect(page.locator('input[name="username"]')).to_have_value("profileuser")
    expect(page.locator('input[name="email"]')).to_have_value("profile@example.com")
    expect(page.locator('input[name="first_name"]')).to_have_value("Profile")
    expect(page.locator('input[name="last_name"]')).to_have_value("User")
    
    # Update profile information
    page.fill('input[name="first_name"]', "UpdatedProfile")
    page.fill('input[name="last_name"]', "UpdatedUser")
    page.click('#profile-form button[type="submit"]')
    
    # Wait for success message
    expect(page.locator('#profile-message')).to_contain_text("Profile updated successfully")
    
    # Verify the updated data persists
    expect(page.locator('input[name="first_name"]')).to_have_value("UpdatedProfile")
    expect(page.locator('input[name="last_name"]')).to_have_value("UpdatedUser")

@pytest.mark.e2e
def test_profile_basic_functionality(page: Page, fastapi_server):
    """Test basic profile functionality without complex validation"""
    
    # Register and login first
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "basicuser")
    page.fill('input[name="email"]', "basic@example.com")
    page.fill('input[name="first_name"]', "Basic")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "basicuser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Navigate to profile
    page.goto(f"{fastapi_server}profile")
    
    # Wait for profile to load
    page.wait_for_timeout(2000)
    
    # Verify profile form elements are present
    expect(page.locator('input[name="first_name"]')).to_be_visible()
    expect(page.locator('input[name="last_name"]')).to_be_visible()
    expect(page.locator('input[name="username"]')).to_be_visible()
    expect(page.locator('input[name="email"]')).to_be_visible()
    expect(page.locator('#profile-form button[type="submit"]')).to_be_visible()
    
    # Verify password change form elements are present
    expect(page.locator('input[name="current_password"]')).to_be_visible()
    expect(page.locator('input[name="new_password"]')).to_be_visible()
    expect(page.locator('input[name="confirm_new_password"]')).to_be_visible()
    expect(page.locator('#password-form button[type="submit"]')).to_be_visible()

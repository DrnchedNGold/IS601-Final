import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_exponentiation_calculation_flow(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Register a new user
        page.goto(f"{live_server}/register")
        page.fill('input[name="first_name"]', "ExpE2E")
        page.fill('input[name="last_name"]', "User")
        page.fill('input[name="email"]', "expe2euser@example.com")
        page.fill('input[name="username"]', "expe2euser")
        page.fill('input[name="password"]', "ExpE2Epass123!")
        page.fill('input[name="confirm_password"]', "ExpE2Epass123!")
        page.click('button[type="submit"]')
        # Login
        page.goto(f"{live_server}/login")
        page.fill('input[name="username"]', "expe2euser")
        page.fill('input[name="password"]', "ExpE2Epass123!")
        page.click('button[type="submit"]')
        # Go to dashboard and select exponentiation
        page.goto(f"{live_server}/dashboard")
        page.select_option('#calcType', 'exponentiation')
        page.fill('#calcInputs', '2, 8')
        page.click('#calculationForm button[type="submit"]')
        page.wait_for_selector('#successAlert')
        assert "256" in page.inner_text('#successAlert')
        # Check that the calculation appears in the history table
        page.wait_for_selector('#calculationsTable')
        assert "exponentiation" in page.inner_text('#calculationsTable')
        assert "2, 8" in page.inner_text('#calculationsTable')
        assert "256" in page.inner_text('#calculationsTable')
        browser.close()

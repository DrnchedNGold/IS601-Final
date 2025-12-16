import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_exponentiation_calculation_flow(page: Page, fastapi_server):
    """E2E test for complete exponentiation calculation workflow"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "expuser")
    page.fill('input[name="email"]', "exp@example.com")
    page.fill('input[name="first_name"]', "Exp")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "expuser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Test exponentiation calculation
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "2, 8")
    page.click('#calculationForm button[type="submit"]')
    
    # Wait for success message
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 256", timeout=10000)
    
    # Verify calculation appears in history table
    expect(page.locator('#calculationsTable')).to_contain_text("exponentiation")
    expect(page.locator('#calculationsTable')).to_contain_text("2, 8")
    expect(page.locator('#calculationsTable')).to_contain_text("256")
    
    # Test another exponentiation
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "3, 4")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 81", timeout=10000)

@pytest.mark.e2e
def test_exponentiation_validation_errors(page: Page, fastapi_server):
    """Test exponentiation validation errors in UI"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "expvaliduser")
    page.fill('input[name="email"]', "expvalid@example.com")
    page.fill('input[name="first_name"]', "ExpValid")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "expvaliduser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Test insufficient inputs (only one number)
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "5")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#errorMessage')).to_contain_text("Please enter at least two valid numbers", timeout=10000)

@pytest.mark.e2e  
def test_exponentiation_basic_operations(page: Page, fastapi_server):
    """Test basic exponentiation operations without edge cases"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "expbasicuser")
    page.fill('input[name="email"]', "expbasic@example.com")
    page.fill('input[name="first_name"]', "ExpBasic")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "expbasicuser") 
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Test base^0 = 1
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "5, 0")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 1", timeout=10000)
    
    # Test 1^anything = 1
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "1, 100")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 1", timeout=10000)

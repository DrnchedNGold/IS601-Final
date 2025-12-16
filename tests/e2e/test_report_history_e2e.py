import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_report_history_metrics_display(page: Page, fastapi_server):
    """E2E test for report/history metrics display and calculation history"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "reportuser")
    page.fill('input[name="email"]', "report@example.com")
    page.fill('input[name="first_name"]', "Report")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "reportuser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Initially should show no calculations
    expect(page.locator('#metricTotal')).to_contain_text("0")
    expect(page.locator('#metricCommon')).to_contain_text("N/A")
    
    # Perform a calculation to generate data
    page.select_option('select[name="type"]', "addition")
    page.fill('input[name="inputs"]', "10, 20, 30")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 60", timeout=10000)
    
    # Wait for metrics to update and reload
    page.wait_for_timeout(3000)
    page.reload()
    page.wait_for_timeout(2000)
    
    # Check that metrics updated
    expect(page.locator('#metricTotal')).to_contain_text("1")
    expect(page.locator('#metricCommon')).to_contain_text("addition")
    
    # Test calculation history table shows the calculation
    expect(page.locator('#calculationsTable')).to_contain_text("addition")
    expect(page.locator('#calculationsTable')).to_contain_text("10, 20, 30")
    expect(page.locator('#calculationsTable')).to_contain_text("60")

@pytest.mark.e2e
def test_calculation_history_crud_operations(page: Page, fastapi_server):
    """Test CRUD operations in calculation history"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "cruduser")
    page.fill('input[name="email"]', "crud@example.com")
    page.fill('input[name="first_name"]', "CRUD")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "cruduser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Create a calculation
    page.select_option('select[name="type"]', "division")
    page.fill('input[name="inputs"]', "100, 4")
    page.click('#calculationForm button[type="submit"]')
    
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 25", timeout=10000)
    
    # Verify it appears in the table
    expect(page.locator('#calculationsTable')).to_contain_text("division")
    expect(page.locator('#calculationsTable')).to_contain_text("100, 4")
    expect(page.locator('#calculationsTable')).to_contain_text("25")
    
    # Test View button exists
    expect(page.locator('a:has-text("View")')).to_be_visible()
    
    # Test Edit button exists  
    expect(page.locator('a:has-text("Edit")')).to_be_visible()

@pytest.mark.e2e
def test_empty_state_displays(page: Page, fastapi_server):
    """Test that empty states display correctly"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "emptyuser")
    page.fill('input[name="email"]', "empty@example.com")
    page.fill('input[name="first_name"]', "Empty")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "emptyuser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Check empty state for metrics
    expect(page.locator('#metricTotal')).to_contain_text("0")
    expect(page.locator('#metricAvg')).to_contain_text("0.00")
    expect(page.locator('#metricCommon')).to_contain_text("N/A")
    expect(page.locator('#metricLast')).to_contain_text("N/A")
    
    # Check empty state for calculations table
    expect(page.locator('#calculationsTable')).to_contain_text("No calculations found")

@pytest.mark.e2e
def test_mixed_calculation_types_metrics(page: Page, fastapi_server):
    """Test metrics with various calculation types including exponentiation"""
    
    # Register and login
    page.goto(f"{fastapi_server}register")
    page.fill('input[name="username"]', "mixeduser")
    page.fill('input[name="email"]', "mixed@example.com")
    page.fill('input[name="first_name"]', "Mixed")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="password"]', "TestPass123!")
    page.fill('input[name="confirm_password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/login", timeout=10000)
    
    page.fill('input[name="username"]', "mixeduser")
    page.fill('input[name="password"]', "TestPass123!")
    page.click('button[type="submit"]')
    
    page.wait_for_url("**/dashboard", timeout=10000)
    
    # Do exponentiation calculation
    page.select_option('select[name="type"]', "exponentiation")
    page.fill('input[name="inputs"]', "2, 3")
    page.click('#calculationForm button[type="submit"]')
    expect(page.locator('#successMessage')).to_contain_text("Calculation complete: 8", timeout=10000)
    
    page.wait_for_timeout(3000)
    page.reload()
    page.wait_for_timeout(2000)
    
    # Check metrics
    expect(page.locator('#metricTotal')).to_contain_text("1")
    expect(page.locator('#metricCommon')).to_contain_text("exponentiation")
    
    # Verify calculation appears in history
    expect(page.locator('#calculationsTable')).to_contain_text("exponentiation")
    expect(page.locator('#calculationsTable')).to_contain_text("2, 3")
    expect(page.locator('#calculationsTable')).to_contain_text("8")

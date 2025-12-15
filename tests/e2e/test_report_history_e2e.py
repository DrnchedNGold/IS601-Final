import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_report_history_metrics_display(live_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Register and login
        page.goto(f"{live_server}/register")
        page.fill('input[name="first_name"]', "ReportE2E")
        page.fill('input[name="last_name"]', "User")
        page.fill('input[name="email"]', "reporte2euser@example.com")
        page.fill('input[name="username"]', "reporte2euser")
        page.fill('input[name="password"]', "ReportE2Epass123!")
        page.fill('input[name="confirm_password"]', "ReportE2Epass123!")
        page.click('button[type="submit"]')
        page.goto(f"{live_server}/login")
        page.fill('input[name="username"]', "reporte2euser")
        page.fill('input[name="password"]', "ReportE2Epass123!")
        page.click('button[type="submit"]')
        page.goto(f"{live_server}/dashboard")
        # Add a calculation
        page.select_option('#calcType', 'addition')
        page.fill('#calcInputs', '1, 2')
        page.click('#calculationForm button[type="submit"]')
        page.wait_for_selector('#successAlert')
        # Check usage metrics
        page.wait_for_selector('#usageMetricsCard')
        total = page.inner_text('#metricTotal')
        avg = page.inner_text('#metricAvg')
        common = page.inner_text('#metricCommon')
        last = page.inner_text('#metricLast')
        assert total == "1"
        assert float(avg) >= 2.0
        assert "addition" in common
        assert last != "-"
        browser.close()

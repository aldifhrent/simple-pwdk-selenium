import pytest
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from util.sidebar import Sidebar

@pytest.mark.smoke
@pytest.mark.reports
def test_reports_page(driver, app_url, creds):
    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    # Navigasi ke Reports via Sidebar
    sidebar = Sidebar(driver)
    sidebar.go_to_reports()

    rp = ReportPage(driver)
    rp.wait_for_page()

    # --- Verifikasi Header ---
    title, desc = rp.get_header_text()
    assert title == "Sales Reports"
    assert "Track your business performance" in desc

    # --- Verifikasi Filter ---
    options = rp.get_filter_options()
    expected_filters = ["Today", "Last 7 Days", "This Month", "This Year"]
    for opt in expected_filters:
        assert opt in options

    # --- Cek setiap filter ---
    for filter_value in expected_filters:
        rp.select_filter(filter_value)
        summary = rp.get_summary_cards()
        assert len(summary) == 4  # 4 kartu ringkasan

        daily_sales = rp.get_daily_sales()
        assert all(len(item) == 2 for item in daily_sales)  # Tanggal & nilai

        top_products = rp.get_top_products()
        assert all(len(item) == 3 for item in top_products)  # Nama, sold, total

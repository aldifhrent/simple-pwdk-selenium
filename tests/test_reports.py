import pytest
from pages.login_page import LoginPage
from pages.report_page import ReportPage
from util.sidebar import Sidebar

@pytest.mark.reports
def test_reports_page_header_and_filters(driver, app_url, creds):
    """Positive test: login, header, dan filter muncul sesuai requirement"""

    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    # Navigasi ke Reports
    sidebar = Sidebar(driver)
    sidebar.go_to_reports()

    rp = ReportPage(driver)
    rp.wait_for_page()

    # --- Header ---
    title, desc = rp.get_header_text()
    assert title == "Sales Reports"
    assert "Track your business performance" in desc

    # --- Filter tersedia ---
    options = rp.get_filter_options()
    expected_filters = ["Today", "Last 7 Days", "This Month", "This Year"]
    for opt in expected_filters:
        assert opt in options


@pytest.mark.reports
@pytest.mark.parametrize("filter_value", ["Today", "Last 7 Days", "This Month", "This Year"])
def test_reports_page_summary_and_data(driver, app_url, creds, filter_value):
    """Positive test: setiap filter menampilkan summary cards, daily sales, top products"""

    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    # Navigasi ke Reports
    sidebar = Sidebar(driver)
    sidebar.go_to_reports()

    rp = ReportPage(driver)
    rp.wait_for_page()

    # --- Pilih filter ---
    rp.select_filter(filter_value)

    # --- Summary cards ---
    summary = rp.get_summary_cards()
    assert len(summary) == 4  # Revenue, Orders, Customers, Profit

    # --- Daily Sales ---
    daily_sales = rp.get_daily_sales()
    assert all(len(item) == 2 for item in daily_sales)  # (tanggal, nilai)

    # --- Top Products ---
    top_products = rp.get_top_products()
    assert all(len(item) == 3 for item in top_products)  # (nama produk, sold, total revenue)


# ---------------- NEGATIVE CASES ---------------- #
@pytest.mark.reports
def test_reports_missing_filter(driver, app_url, creds):
    """Negative test: jika filter kurang dari 4 maka dianggap bug"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    sidebar = Sidebar(driver)
    sidebar.go_to_reports()

    rp = ReportPage(driver)
    rp.wait_for_page()

    options = rp.get_filter_options()
    assert len(options) == 4, f"BUG: Jumlah filter salah, dapat {len(options)}"


@pytest.mark.reports
def test_reports_summary_card_incorrect(driver, app_url, creds):
    """Negative test: jumlah summary card tidak sesuai"""

    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    sidebar = Sidebar(driver)
    sidebar.go_to_reports()

    rp = ReportPage(driver)
    rp.wait_for_page()

    summary = rp.get_summary_cards()
    assert len(summary) == 4, f"BUG: Jumlah summary cards salah, dapat {len(summary)}"

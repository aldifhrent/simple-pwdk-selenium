import logging
import pytest
from pages.login_page import LoginPage
from pages.opt.transactions_page import TransactionsPage
from util.sidebar import Sidebar

logger = logging.getLogger(__name__)

@pytest.mark.optional
def test_view_and_filter_transactions(driver, app_url, creds):
    logger.info("🔹 Mulai test Transactions (view + filter)")

    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    # Pakai Sidebar helper untuk ke Transactions
    sidebar = Sidebar(driver)
    sidebar.click_menu("Transactions")

    tp = TransactionsPage(driver)
    tp.assert_on_transactions_page()

    # Filter transaksi
    tp.filter_by_time("All Time")

    # Cari transaksi tertentu
    txn_id = "TXN-20250811"  # contoh partial TXN ID
    tp.search_transaction(txn_id)
    tp.assert_transaction_visible(txn_id)

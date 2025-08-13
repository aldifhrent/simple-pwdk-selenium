import logging
import pytest
import os
from pages.login_page import LoginPage
from pages.pos_page import PosPage

logger = logging.getLogger(__name__)

def take_screenshot(driver, name):
    os.makedirs("screenshots/transactions", exist_ok=True)
    driver.save_screenshot(f"screenshots/transactions/{name}.png")

@pytest.mark.smoke
@pytest.mark.checkout
def test_checkout_with_cash(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"

    # Tambahkan produk ke cart
    pp.search_product(product)
    pp.add_to_cart(product)

    # Checkout flow
    pp.checkout()
    pp.fill_customer_info("John Doe", "john@example.com")
    pp.select_payment_method("Cash")
    pp.complete_transaction()

    # Verifikasi transaksi
    alert_text, txid = pp.get_transaction_alert_and_id()

    assert alert_text is not None, "Alert tidak muncul"
    assert txid is not None, f"TXID tidak ditemukan di alert: {alert_text}"

    logger.info(f"✅ Checkout sukses, TXID: {txid}")

    take_screenshot(driver, "checkout_cash")

import logging
import pytest
import os
from pages.login_page import LoginPage
from pages.pos_page import PosPage
from util.helper import take_screenshot
from pages.cart_page import CartPage
logger = logging.getLogger(__name__)

@pytest.mark.checkout
def test_checkout_with_name_and_email(driver, app_url, creds):
    """Case 1: Nama & Email terisi → Expected sukses"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    cp = CartPage(driver)
    pp.search_product("Wireless Headphones")
    pp.add_to_cart("Wireless Headphones")
    cp.checkout()
    cp.fill_customer_info("John Doe", "john@example.com")
    cp.select_payment_method("Cash")
    cp.complete_transaction()

    alert_text, txid = cp.get_transaction_alert_and_id()

    assert alert_text is not None, "Expected sukses tapi tidak ada alert"
    assert txid is not None, f"Expected sukses tapi TXID tidak ditemukan. Alert: {alert_text}"
    logger.info(f"✅ Checkout sukses (John Doe, john@example.com), TXID: {txid}")
    take_screenshot(driver, "checkout_name_email", folder="screenshots/checkout")


@pytest.mark.checkout
def test_checkout_with_empty_fields(driver, app_url, creds):
    """Case 2: Kosong semua → Expected gagal"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    cp = CartPage(driver)
    pp.search_product("Wireless Headphones")
    pp.add_to_cart("Wireless Headphones")
    cp.checkout()
    cp.fill_customer_info("", "")
    cp.select_payment_method("Cash")
    cp.complete_transaction()

    alert_text, txid = cp.get_transaction_alert_and_id()

    if alert_text and txid:
        pytest.fail("BUG: Checkout berhasil walau nama & email kosong")
    logger.info("✅ Validasi berhasil: Checkout gagal seperti yang diharapkan (kosong semua)")
    take_screenshot(driver, "checkout_empty_fields" , folder="screenshots/checkout")


@pytest.mark.checkout
def test_checkout_with_name_only(driver, app_url, creds):
    """Case 3: Hanya nama → Expected gagal"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    cp = CartPage(driver)
    pp.search_product("Wireless Headphones")
    pp.add_to_cart("Wireless Headphones")
    cp.checkout()
    cp.fill_customer_info("John Doe", "")
    cp.select_payment_method("Cash")
    cp.complete_transaction()

    alert_text, txid = cp.get_transaction_alert_and_id()

    if alert_text and txid:
        pytest.fail("BUG: Checkout berhasil walau hanya nama")
    logger.info("✅ Validasi berhasil: Checkout gagal seperti yang diharapkan (nama saja)")
    take_screenshot(driver, "checkout_name_only" , folder="screenshots/checkout")


@pytest.mark.checkout
def test_checkout_with_email_only(driver, app_url, creds):
    """Case 4: Hanya email → Expected gagal"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    cp = CartPage(driver)
    pp.search_product("Wireless Headphones")    
    pp.add_to_cart("Wireless Headphones")
    cp.checkout()
    cp.fill_customer_info("", "john@example.com")
    cp.select_payment_method("Cash")
    cp.complete_transaction()

    alert_text, txid = cp.get_transaction_alert_and_id()


    if alert_text and txid:
        pytest.fail("BUG: Checkout berhasil walau hanya email")
    logger.info("✅ Validasi berhasil: Checkout gagal seperti yang diharapkan (email saja)")
    take_screenshot(driver, "checkout_email_only" , folder="screenshots/checkout")
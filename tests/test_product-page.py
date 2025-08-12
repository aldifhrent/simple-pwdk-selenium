# tests/test_search_add.py
import logging
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

logger = logging.getLogger(__name__)

def test_search_and_add_wireless_headphones(driver, app_url, creds):
    # 1) Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()  # atau lp.assert_logged_in() kalau pakai versi itu

    # 2) Search produk
    pp = ProductsPage(driver)
    product_name = "Wireless Headphones"
    pp.search(product_name)
    pp.assert_card_visible(product_name)

    # (opsional) cek price & stock dari card
    price = pp.get_price_text(product_name)
    stock = pp.get_stock_number(product_name)
    logger.info("Found product: %s | price=%s | stock=%s", product_name, price, stock)

    # 3) Add to Cart
    pp.add_to_cart_by_name(product_name)

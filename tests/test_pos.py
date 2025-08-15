import logging
import pytest
import os
from datetime import datetime
from pages.login_page import LoginPage
from pages.pos_page import PosPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

@pytest.mark.smoke
@pytest.mark.products
def test_product_search(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)

    search_name = "Wireless"
    pp.search_product(search_name)

    pp.assert_product_visible("Wireless Headphones")

    take_screenshot(driver, "product_search_wireless", folder="screenshots/pos")

@pytest.mark.products
def test_product_search_with_category_filter(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)

    category_name = "Electronics"
    pp.filter_by_category(category_name)

    # Verifikasi produk ada
    pp.assert_product_visible("Wireless Headphones", folder="screenshots/pos")

    take_screenshot(driver, "product_search_filter_electronics")

@pytest.mark.products
@pytest.mark.negative
def test_product_search_not_found(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)

    search_name = "XYZ"  # Nama produk yang pasti tidak ada
    pp.search_product(search_name)

    assert pp.is_no_products_found(), f"Expected 'No products found' saat cari '{search_name}'"

    take_screenshot(driver, "product_search_not_found" , folder="screenshots/pos")

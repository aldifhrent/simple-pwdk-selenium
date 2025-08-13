# tests/test_cart.py
import logging
import pytest
import os

from pages.login_page import LoginPage
from pages.pos_page import PosPage

logger = logging.getLogger(__name__)

def take_screenshot(driver, name):
    os.makedirs("screenshots/cart", exist_ok=True)
    driver.save_screenshot(f"screenshots/cart/{name}.png")

@pytest.mark.cart
def test_add_to_cart_only(driver, app_url, creds):
    """1. Add to cart saja"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.select_product(product)
    take_screenshot(driver, "add_only")


@pytest.mark.cart
def test_add_and_increase(driver, app_url, creds):
    """2. Add to cart lalu increase"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.select_product(product)
    pp.increase_quantity(product)
    take_screenshot(driver, "add_increase")


@pytest.mark.cart
def test_add_and_decrease(driver, app_url, creds):
    """3. Add to cart lalu decrease"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.select_product(product)
    pp.decrease_quantity(product)
    take_screenshot(driver, "add_decrease")


@pytest.mark.cart
def test_add_and_remove(driver, app_url, creds):
    """4. Add to cart lalu remove"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.select_product(product)
    pp.remove_from_cart(product)
    take_screenshot(driver, "add_remove")

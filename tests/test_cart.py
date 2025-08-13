# tests/test_cart.py
import logging
import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)

@pytest.fixture
def login_and_cart(driver, app_url, creds):
    """Login lalu return instance CartPage."""
    login_page = LoginPage(driver)
    login_page.visit(app_url)
    login_page.login(creds["email"], creds["password"])
    login_page.wait_no_error()
    return CartPage(driver)

@pytest.mark.cart
def test_add_to_cart_then_finish(login_and_cart):
    """1. Add to cart terus selesai."""
    cart_page = login_and_cart
    cart_page.add_product_to_cart("Wireless Headphones")
    assert cart_page.get_cart_items_count() == 1
    logger.info("✅ Add to cart selesai")

@pytest.mark.cart
def test_add_to_cart_then_decrease(login_and_cart):
    """2. Add to cart lalu decrease."""
    cart_page = login_and_cart
    cart_page.add_product_to_cart("Wireless Headphones")
    cart_page.increase_quantity("Wireless Headphones")  # supaya bisa dikurangi
    old_count = cart_page.get_cart_items_count()

    cart_page.decrease_quantity("Wireless Headphones")
    assert cart_page.get_cart_items_count() < old_count
    logger.info("✅ Add to cart + decrease berhasil")

@pytest.mark.cart
def test_add_to_cart_then_increase(login_and_cart):
    """3. Add to cart lalu increase."""
    cart_page = login_and_cart
    cart_page.add_product_to_cart("Wireless Headphones")
    old_count = cart_page.get_cart_items_count()

    cart_page.increase_quantity("Wireless Headphones")
    assert cart_page.get_cart_items_count() > old_count
    logger.info("✅ Add to cart + increase berhasil")

@pytest.mark.cart
def test_add_to_cart_then_remove(login_and_cart):
    """4. Add to cart lalu remove."""
    cart_page = login_and_cart
    cart_page.add_product_to_cart("Wireless Headphones")
    cart_page.remove_product("Wireless Headphones")
    assert cart_page.get_cart_items_count() == 0
    logger.info("✅ Add to cart + remove berhasil")

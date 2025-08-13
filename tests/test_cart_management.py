import logging
import pytest
import os
from pages.login_page import LoginPage
from pages.pos_page import PosPage

logger = logging.getLogger(__name__)

def take_screenshot(driver, name):
    os.makedirs("screenshots/cart", exist_ok=True)
    driver.save_screenshot(f"screenshots/cart/{name}.png")

@pytest.mark.smoke
@pytest.mark.cart
def test_add_and_increase(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"

    # Step 1: Cari produk
    pp.search_product(product)

    # Step 2: Add to Cart
    pp.add_to_cart(product)

    # Step 3: Increase Quantity
    pp.increase_quantity(product)

    # Step 4: Screenshot hasil
    take_screenshot(driver, "add_and_increase")

@pytest.mark.smoke
@pytest.mark.cart
def test_add_increase_decrease(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"

    # Step 1: Cari produk
    pp.search_product(product)

    # Step 2: Add to Cart
    pp.add_to_cart(product)

    # Step 3: Increase Quantity
    pp.increase_quantity(product)

    # Step 4: Decrease Quantity
    pp.decrease_quantity(product)

    # Step 5: Screenshot hasil
    take_screenshot(driver, "add_increase_decrease")

@pytest.mark.smoke
@pytest.mark.cart
def test_add_and_remove(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"

    # Add to cart
    pp.search_product(product)
    pp.select_product(product)

    # Remove from cart
    pp.remove_product(product)

    # Verifikasi cart kosong
    assert pp.get_cart_items_count() == 0, "Cart seharusnya kosong setelah item dihapus"
    logger.info("✅ Item berhasil dihapus dari cart")

    take_screenshot(driver, "remove_item")
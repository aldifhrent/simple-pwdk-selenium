import logging
import pytest
from pages.login_page import LoginPage
from pages.pos_page import PosPage
from pages.cart_page import CartPage
from util.helper import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
logger = logging.getLogger(__name__)

# @pytest.fixture
def login_and_add_product(driver, app_url, creds):
    """Login dan tambah produk ke cart"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.add_to_cart(product)
    return product

@pytest.mark.smoke
@pytest.mark.cart
def test_add_and_increase(driver, app_url, creds, login_and_add_product):
    product = login_and_add_product
    cp = CartPage(driver)

    cp.increase_quantity(product)
    take_screenshot(driver, "add_and_increase", folder="screenshots/cart")

@pytest.mark.smoke
@pytest.mark.cart
def test_add_increase_decrease(driver, app_url, creds, login_and_add_product):
    product = login_and_add_product
    cp = CartPage(driver)

    cp.increase_quantity(product)
    cp.decrease_quantity(product)
    take_screenshot(driver, "add_increase_decrease", folder="screenshots/cart")

@pytest.mark.smoke
@pytest.mark.cart
def test_add_and_remove(driver, app_url, creds, login_and_add_product):
    product = login_and_add_product
    cp = CartPage(driver)

    cp.remove_product(product)
    assert cp.get_cart_items_count() == 0, "Cart seharusnya kosong setelah item dihapus"
    logger.info("✅ Item berhasil dihapus dari cart")
    take_screenshot(driver, "remove_item", folder="screenshots/cart")

# Negative Case
@pytest.mark.cart
@pytest.mark.negative
def test_cart_empty_state(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()

    title, desc = cp.get_cart_empty_state()
    assert title == "Your cart is empty", f"Expected 'Your cart is empty', got {title}"
    assert "Add products to get started" in desc
    logger.info("✅ Validasi cart kosong berhasil")
    take_screenshot(driver, "cart_empty_state", folder="screenshots/cart")

@pytest.mark.cart
@pytest.mark.negative
def test_increase_quantity_beyond_stock(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)
    product = "Cotton T-Shirt"  # pastikan stok > 1
    pp.search_product(product)
    pp.add_to_cart(product)

    cp = CartPage(driver)
    cp.increase_quantity_to_max(product)

    # Tunggu sampai tombol plus disabled
    plus_button_locator = (
        By.XPATH,
        f"//h3[normalize-space()='{product}']/ancestor::div[contains(@class,'flex items-center')]//button[.//svg[contains(@class,'lucide-plus')]]"
    )
    WebDriverWait(driver, 5).until(
        EC.element_attribute_to_include(plus_button_locator, "disabled")
    )

    assert cp.is_increase_disabled(product), "Expected tombol '+' disabled saat stok habis"

@pytest.mark.cart
@pytest.mark.negative
def test_decrease_quantity_to_zero(driver, app_url, creds, login_and_add_product):
    product = login_and_add_product
    cp = CartPage(driver)

    cp.decrease_quantity_to_zero(product)
    assert cp.get_cart_items_count() == 0, "Expected cart kosong setelah qty jadi 0"
    logger.info("✅ Item otomatis terhapus setelah qty 0")
    take_screenshot(driver, "decrease_qty_to_zero", folder="screenshots/cart")

@pytest.mark.cart
@pytest.mark.negative
def test_remove_from_empty_cart(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()

    cp.try_remove_when_empty()
    assert cp.get_cart_items_count() == 0, "Cart harus tetap kosong"
    logger.info("✅ Remove saat cart kosong tidak error")
    take_screenshot(driver, "remove_empty_cart", folder="screenshots/cart")

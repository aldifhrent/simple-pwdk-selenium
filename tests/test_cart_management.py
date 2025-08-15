import logging
import pytest
from pages.login_page import LoginPage
from pages.pos_page import PosPage
from pages.cart_page import CartPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

@pytest.fixture
def login_and_add_product(driver, app_url, creds):
    """Login dan tambah produk ke cart"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()
    logger.info("✅ Login berhasil")

    pp = PosPage(driver)
    product = "Wireless Headphones"
    pp.search_product(product)
    pp.add_to_cart(product)
    logger.info(f"✅ Produk '{product}' ditambahkan ke cart")
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
    assert cp.get_cart_items_count() == 0
    logger.info("✅ Item berhasil dihapus dari cart")
    take_screenshot(driver, "remove_item", folder="screenshots/cart")

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
    assert title == "Your cart is empty"
    assert "Add products to get started" in desc
    logger.info("✅ Validasi cart kosong berhasil")
    take_screenshot(driver, "cart_empty_state", folder="screenshots/cart")

@pytest.mark.cart
@pytest.mark.negative
def test_increase_quantity_until_disabled(driver, app_url, creds):
    logger.info("=== START test_increase_quantity_until_disabled ===")

    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()
    logger.info("✅ Login berhasil")

    # Pilih produk dengan stok > 1
    product = "Coffee Beans"
    pp = PosPage(driver)
    pp.search_product(product)
    pp.add_to_cart(product)
    logger.info(f"✅ Produk '{product}' berhasil ditambahkan ke cart")

    # Pastikan produk ada di cart
    cp = CartPage(driver)
    assert cp.find_product_in_cart(product), f"Produk {product} tidak ditemukan di cart"
    logger.info(f"✅ Produk '{product}' ditemukan di cart")

    # Debug: tampilkan struktur cart
    cp.debug_cart_structure(product)
    
    # Cek quantity awal
    initial_qty = cp.get_product_quantity_in_cart(product)
    logger.info(f"✅ Quantity awal {product}: {initial_qty}")

    # Increase quantity sampai stok habis atau tombol disabled
    cp.increase_quantity_to_max(product)

    # Assert di cart → tombol '+' disabled
    assert cp.is_increase_disabled(product), "Expected tombol '+' di cart disabled saat stok habis"

    logger.info("=== END test_increase_quantity_until_disabled ===")

@pytest.mark.cart
@pytest.mark.negative
def test_decrease_quantity_to_zero(driver, app_url, creds, login_and_add_product):
    product = login_and_add_product
    cp = CartPage(driver)
    cp.decrease_quantity_to_zero(product)
    assert cp.get_cart_items_count() == 0
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
    assert cp.get_cart_items_count() == 0
    logger.info("✅ Remove saat cart kosong tidak error")
    take_screenshot(driver, "remove_empty_cart", folder="screenshots/cart")

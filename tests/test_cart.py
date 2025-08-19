import logging
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from util.helper import take_screenshot

# =======================
# LOGGER CONFIG
# =======================
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # default: hanya WARNING ke atas yang tampil
# kalau mau debug qty, ganti ke DEBUG:
# logger.setLevel(logging.DEBUG)

# =======================
# FIXTURES
# =======================
@pytest.fixture
def login_and_empty_cart(driver, app_url, creds):
    """Login dan pastikan cart kosong."""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()

    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong"
    return cp


@pytest.fixture
def login_add_product(driver, app_url, creds, request):
    """Login, kosongkan cart, lalu tambah produk tertentu."""
    product = request.param

    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()

    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong sebelum tambah produk"

    pp = ProductsPage(driver)
    pp.search_product(product)
    pp.add_to_cart(product)

    # Tunggu hingga cart terupdate (lebih stabil dari time.sleep)
    WebDriverWait(driver, 5).until(lambda d: cp.get_cart_items_count() > 0)

    return cp

# =======================
# POSITIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_add_and_increase(login_add_product, driver):
    cp = login_add_product
    qty_before = cp.get_quantity()
    cp.increase_quantity()
    qty_after = cp.get_quantity()
    assert qty_after == qty_before + 1, f"Quantity harus naik dari {qty_before} ke {qty_before+1}"
    take_screenshot(driver, "add_and_increase", folder="screenshots/cart")


@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_add_increase_decrease(login_add_product, driver):
    cp = login_add_product
    cp.increase_quantity()
    cp.decrease_quantity()
    qty = cp.get_quantity()
    assert qty == 1, f"Quantity akhir harus kembali ke 1, tapi dapat {qty}"
    take_screenshot(driver, "add_increase_decrease", folder="screenshots/cart")


@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Coffee Beans"], indirect=True)
def test_add_and_remove(login_add_product, driver):
    cp = login_add_product
    cp.remove_product()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong setelah remove"
    take_screenshot(driver, "add_and_remove", folder="screenshots/cart")

# =======================
# NEGATIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.negative
def test_cart_empty_state(login_and_empty_cart, driver):
    cp = login_and_empty_cart
    title = cp.get_cart_empty_state()
    assert title == "Your cart is empty"
    take_screenshot(driver, "cart_empty_state", folder="screenshots/cart")

@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product", ["Coffee Beans"], indirect=True)
def test_increase_quantity_until_disabled(login_add_product, driver):
    cp = login_add_product
    cp.increase_quantity_to_max()
    assert cp.is_increase_disabled(), "Tombol + harus disabled di stok max"
    take_screenshot(driver, "increase_until_disabled", folder="screenshots/cart")


@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_decrease_quantity_to_zero(login_add_product, driver):
    cp = login_add_product
    cp.decrease_quantity_to_zero()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong setelah qty=0"
    take_screenshot(driver, "decrease_qty_to_zero", folder="screenshots/cart")


@pytest.mark.cart
@pytest.mark.negative
def test_remove_from_empty_cart(login_and_empty_cart, driver):
    cp = login_and_empty_cart
    cp.try_remove_when_empty()
    assert cp.get_cart_items_count() == 0, "Cart tetap kosong"
    take_screenshot(driver, "remove_empty_cart", folder="screenshots/cart")

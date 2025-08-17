import logging
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

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

    time.sleep(1)  # tunggu UI update
    assert cp.get_cart_items_count() > 0, f"Gagal menambahkan {product} ke cart"
    return product

# =======================
# POSITIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_add_and_increase(driver, login_add_product):
    cp = CartPage(driver)
    qty_before = cp.get_quantity()
    cp.increase_quantity()
    qty_after = cp.get_quantity()
    assert qty_after == qty_before + 1, f"Quantity harus naik dari {qty_before} ke {qty_before+1}"
    take_screenshot(driver, "add_and_increase")

@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_add_increase_decrease(driver, login_add_product):
    cp = CartPage(driver)
    cp.increase_quantity()
    cp.decrease_quantity()
    qty = cp.get_quantity()
    assert qty == 1, f"Quantity akhir harus kembali ke 1, tapi dapat {qty}"
    take_screenshot(driver, "add_increase_decrease")

@pytest.mark.cart
@pytest.mark.parametrize("login_add_product", ["Coffee Beans"], indirect=True)
def test_add_and_remove(driver, login_add_product):
    cp = CartPage(driver)
    cp.remove_product()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong setelah remove"
    take_screenshot(driver, "add_and_remove")

# =======================
# NEGATIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.negative
def test_cart_empty_state(login_and_empty_cart):
    cp = login_and_empty_cart
    title = cp.get_cart_empty_state()
    assert title == "Your cart is empty"
    take_screenshot(cp.driver, "cart_empty_state")


@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product", ["Coffee Beans"], indirect=True)
def test_increase_quantity_until_disabled(driver, login_add_product):
    cp = CartPage(driver)
    
    cp.increase_quantity_to_max()
    assert cp.is_increase_disabled(), "Tombol + harus disabled di stok max"
    take_screenshot(driver, "increase_until_disabled")

@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product", ["Wireless Headphones"], indirect=True)
def test_decrease_quantity_to_zero(driver, login_add_product):
    cp = CartPage(driver)
    cp.decrease_quantity_to_zero()
    assert cp.get_cart_items_count() == 0, "Cart harus kosong setelah qty=0"
    take_screenshot(driver, "decrease_qty_to_zero")

@pytest.mark.cart
@pytest.mark.negative
def test_remove_from_empty_cart(login_and_empty_cart):
    cp = login_and_empty_cart
    cp.try_remove_when_empty()
    assert cp.get_cart_items_count() == 0, "Cart tetap kosong"
    take_screenshot(cp.driver, "remove_empty_cart")

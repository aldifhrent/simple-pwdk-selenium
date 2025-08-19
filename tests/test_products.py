import logging
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

# =========================
# FIXTURE LOGIN
# =========================
@pytest.fixture
def login_and_pos(driver, app_url, creds):
    """Login lalu masuk ke halaman POS"""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()
    return ProductsPage(driver)

# =========================
# POSITIVE CASES
# =========================
@pytest.mark.products
@pytest.mark.positive
@pytest.mark.parametrize(
    "search_name, expected_product",
    [
        pytest.param("Wireless", "Wireless Headphones", id="valid-partial"),
        pytest.param("wireless headphones", "Wireless Headphones", id="case-insensitive"),
        pytest.param("Headphones", "Wireless Headphones", id="partial-tail"),
        pytest.param("Wireless Headphones", "Wireless Headphones", id="full-match"),
        pytest.param("Coff", "Coffee Beans", id="partial-coff"),
    ],
)
def test_product_search_and_selection_positive(login_and_pos, search_name, expected_product):
    pp = login_and_pos
    logger.info(f"Searching for product: {search_name}")
    pp.search_product(search_name)
    pp.assert_product_visible(expected_product)

    logger.info(f"Adding product to cart: {expected_product}")
    pp.add_to_cart(expected_product)

    # Verifikasi produk ada di cart
    assert pp.is_product_in_cart(expected_product), f"Produk {expected_product} tidak ada di cart"
    take_screenshot(pp.driver, f"product_search_selection_{search_name}", folder="screenshots/pos")

@pytest.mark.products
@pytest.mark.positive
def test_product_search_with_category_filter(login_and_pos):
    pp = login_and_pos
    category_name = "Electronics"
    pp.filter_by_category(category_name)
    pp.assert_product_visible("Wireless Headphones")

    pp.add_to_cart("Wireless Headphones")
    assert pp.is_product_in_cart("Wireless Headphones"), "Produk tidak masuk ke cart"
    take_screenshot(pp.driver, "product_search_filter_category", folder="screenshots/pos")

# =========================
# NEGATIVE CASES
# =========================
@pytest.mark.products
@pytest.mark.negative
@pytest.mark.parametrize(
    "search_name, expect_no_results",
    [
        pytest.param("NonExistentProduct", True, id="invalid-name"),
        pytest.param("XYZ", True, id="random-text"),
        pytest.param("", False, id="empty-search"),
    ],
)
@pytest.mark.products
@pytest.mark.negative
def test_product_search_negative(login_and_pos, search_name, expect_no_results):
    pp = login_and_pos
    logger.info(f"Searching for product: '{search_name}'")
    pp.search_product(search_name)

    if expect_no_results:
        assert pp.is_no_products_found(), f"Expected 'No products found' saat cari '{search_name}'"
    else:
        assert pp.has_add_to_cart_button(), "Expected ada produk saat search kosong"

    take_screenshot(pp.driver, f"product_search_not_found_{search_name or 'empty'}", folder="screenshots/pos")

@pytest.mark.products
@pytest.mark.negative
def test_no_selection_when_product_not_found(login_and_pos):
    pp = login_and_pos
    search_name = "InvalidSearch123"
    pp.search_product(search_name)

    assert pp.is_no_products_found(), "Expected no products found"
    assert not pp.has_add_to_cart_button(), "Tidak boleh ada tombol Add to Cart saat produk tidak ditemukan"
    take_screenshot(pp.driver, "product_no_selection_invalid_search", folder="screenshots/pos")

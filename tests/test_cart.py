import logging
import pytest
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
    """Login dan kosongkan cart."""
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()
    
    # Verify login success
    actual_header = lp.get_pos_header_text()
    expected_header = "POS System"
    assert actual_header == expected_header, f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
    logger.info("✅ Login berhasil")
    
    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()
    
    # Verify cart is empty
    initial_cart_count = cp.get_cart_items_count()
    logger.info(f"[Fixture] Cart count awal: {initial_cart_count}")
    assert initial_cart_count == 0, f"Cart harus kosong, tapi ada {initial_cart_count} item"
    
    return cp

@pytest.fixture
def login_add_product_empty_cart(driver, app_url, creds, request):
    """Login, kosongkan cart, lalu tambah produk tertentu."""
    product = request.param
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()
    
    # Verify login success
    actual_header = lp.get_pos_header_text()
    expected_header = "POS System"
    assert actual_header == expected_header, f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
    logger.info("✅ Login berhasil")

    cp = CartPage(driver)
    cp.clear_cart_if_not_empty()
    
    # Verify cart is empty
    initial_cart_count = cp.get_cart_items_count()
    logger.info(f"[Fixture] Cart count awal: {initial_cart_count}")
    assert initial_cart_count == 0, f"Cart harus kosong, tapi ada {initial_cart_count} item"

    pp = ProductsPage(driver)
    
    # Step 1: Search product
    logger.info(f"[Fixture] Step 1: Searching product '{product}'")
    pp.search_product(product)
    
    # Step 2: Verify product found
    logger.info(f"[Fixture] Step 2: Verifying product found")
    try:
        pp.assert_product_visible(product)
        logger.info(f"[Fixture] ✅ Product '{product}' ditemukan")
    except Exception as e:
        logger.error(f"[Fixture] ❌ Product '{product}' tidak ditemukan: {e}")
        take_screenshot(driver, f"product_not_found_{product}")
        raise
    
    # Step 3: Add to cart
    logger.info(f"[Fixture] Step 3: Adding product to cart")
    pp.add_to_cart(product)
    
    # Step 4: Wait and verify cart update
    logger.info(f"[Fixture] Step 4: Waiting for cart update")
    import time
    time.sleep(3)  # Added sleep for UI update
    
    # Step 5: Verify product added to cart
    logger.info(f"[Fixture] Step 5: Verifying product added to cart")
    cart_count = cp.get_cart_items_count()
    logger.info(f"[Fixture] Cart count setelah add: {cart_count}")
    
    if cart_count == 0:
        take_screenshot(driver, f"cart_empty_after_add_{product}")
        logger.error(f"[Fixture] ❌ Product '{product}' tidak berhasil ditambahkan ke cart")
        logger.error(f"[Fixture] Cart count: {cart_count}")
        try:
            cart_items = cp.get_cart_items()
            logger.info(f"[Fixture] Cart items found: {len(cart_items)}")
            for i, item in enumerate(cart_items):
                logger.info(f"[Fixture] Cart item {i}: {item.text}")
        except Exception as e:
            logger.error(f"[Fixture] Error getting cart items: {e}")
        raise AssertionError(f"Product {product} tidak berhasil ditambahkan ke cart. Cart count: {cart_count}")
    
    logger.info(f"✅ Produk '{product}' berhasil ditambahkan ke cart. Cart count: {cart_count}")
    return product

# =======================
# POSITIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.parametrize("login_add_product_empty_cart", ["Wireless Headphones"], indirect=True)
def test_add_and_increase(driver, login_add_product_empty_cart):
    """Test adding product and increasing quantity."""
    cp = CartPage(driver)
    
    # Debug cart structure
    cp.debug_cart_structure()
    
    qty_before = cp.get_quantity(0)
    cp.increase_quantity(0)
    qty_after = cp.get_quantity(0)
    assert qty_after == qty_before + 1, f"Quantity should increase from {qty_before} to {qty_before + 1}, but got {qty_after}"
    take_screenshot(driver, "add_and_increase")

@pytest.mark.cart
@pytest.mark.parametrize("login_add_product_empty_cart", ["Wireless Headphones"], indirect=True)
def test_add_increase_decrease(driver, login_add_product_empty_cart):
    """Test adding product, increasing, then decreasing quantity."""
    cp = CartPage(driver)
    cp.increase_quantity(0)
    cp.decrease_quantity(0)
    final_qty = cp.get_quantity(0)
    assert final_qty == 1, f"Final quantity should be 1, but got {final_qty}"
    take_screenshot(driver, "add_increase_decrease")

@pytest.mark.cart
@pytest.mark.parametrize("login_add_product_empty_cart", ["Coffee Beans"], indirect=True)
def test_add_and_remove(driver, login_add_product_empty_cart):
    """Test adding product then removing it."""
    cp = CartPage(driver)
    cp.remove_product(0)
    cart_count = cp.get_cart_items_count()
    assert cart_count == 0, f"Cart should be empty after removal, but has {cart_count} items"
    take_screenshot(driver, "add_and_remove")

# =======================
# NEGATIVE TESTS
# =======================
@pytest.mark.cart
@pytest.mark.negative
def test_cart_empty_state(login_and_empty_cart):
    """Test empty cart state display."""
    cp = login_and_empty_cart
    title, desc = cp.get_cart_empty_state()
    assert title == "Your cart is empty", f"Expected 'Your cart is empty', got '{title}'"
    assert "Add products" in desc, f"Description should contain 'Add products', got '{desc}'"
    take_screenshot(cp.driver, "cart_empty_state")

@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product_empty_cart", ["Coffee Beans"], indirect=True)
def test_increase_quantity_until_disabled(driver, login_add_product_empty_cart):
    """Test increasing quantity until button is disabled."""
    cp = CartPage(driver)
    cp.increase_quantity_to_max(0)
    is_disabled = cp.is_increase_disabled(0)
    assert is_disabled, "Increase button should be disabled after reaching maximum"
    take_screenshot(driver, "increase_until_disabled")

@pytest.mark.cart
@pytest.mark.negative
@pytest.mark.parametrize("login_add_product_empty_cart", ["Wireless Headphones"], indirect=True)
def test_decrease_quantity_to_zero(driver, login_add_product_empty_cart):
    """Test decreasing quantity to zero and item being removed from cart."""
    cp = CartPage(driver)
    
    # Decrease quantity from 1 to 0 (should remove item)
    cp.decrease_quantity(0)
    
    # Verify item is removed from cart (quantity 0 = item removed)
    cart_count = cp.get_cart_items_count()
    assert cart_count == 0, f"Cart should be empty after decreasing quantity to 0, but has {cart_count} items"
    take_screenshot(driver, "decrease_qty_to_zero")

@pytest.mark.cart
@pytest.mark.negative
def test_remove_from_empty_cart(login_and_empty_cart):
    """Test trying to remove from empty cart."""
    cp = login_and_empty_cart
    cp.try_remove_when_empty()
    cart_count = cp.get_cart_items_count()
    assert cart_count == 0, f"Cart should remain empty, but has {cart_count} items"
    take_screenshot(cp.driver, "remove_empty_cart")

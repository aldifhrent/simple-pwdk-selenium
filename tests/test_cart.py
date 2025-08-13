import logging
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

logger = logging.getLogger(__name__)

# ============================================================================
# CART TEST - 3 FUNGSI SAJA: ADD, REMOVE, UPDATE
# ============================================================================

def test_add_item(driver, app_url, creds):
    """Test add item to cart."""
    logger.info("=== TEST: ADD ITEM TO CART ===")
    
    try:
        # Login
        login_page = LoginPage(driver)
        login_page.visit(app_url)
        login_page.login(creds["email"], creds["password"])
        login_page.wait_no_error()
        
        # Verify login
        actual_header = login_page.get_pos_header_text()
        expected_header = "POS System"
        assert actual_header == expected_header, f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
        logger.info("✅ Login successful")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find first product card
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.bg-white")
        logger.info(f"Found {len(product_cards)} product cards")
        
        if len(product_cards) == 0:
            logger.error("❌ No product cards found")
            return
        
        # Find card with button
        first_card = None
        for card in product_cards:
            try:
                button = card.find_element(By.TAG_NAME, "button")
                first_card = card
                logger.info("✅ Found card with button")
                break
            except:
                continue
        
        if not first_card:
            logger.error("❌ No card with button found")
            return
        
        # Add to cart
        add_to_cart_btn = first_card.find_element(By.TAG_NAME, "button")
        add_to_cart_btn.click()
        logger.info("✅ Clicked Add to Cart button")
        
        # Wait for cart to update
        time.sleep(3)
        
        
        logger.info("🎯 Add item test completed!")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        try:
            logger.info("Error" )
        except:
            pass
        raise

def test_remove_item(driver, app_url, creds):
    """Test remove item from cart."""
    logger.info("=== TEST: REMOVE ITEM FROM CART ===")
    
    try:
        # Login
        login_page = LoginPage(driver)
        login_page.visit(app_url)
        login_page.login(creds["email"], creds["password"])
        login_page.wait_no_error()
        
        # Verify login
        actual_header = login_page.get_pos_header_text()
        expected_header = "POS System"
        assert actual_header == expected_header, f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
        logger.info("✅ Login successful")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find first product card
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.bg-white")
        logger.info(f"Found {len(product_cards)} product cards")
        
        if len(product_cards) == 0:
            logger.error("❌ No product cards found")
            return
        
        # Find card with button
        first_card = None
        for card in product_cards:
            try:
                button = card.find_element(By.TAG_NAME, "button")
                first_card = card
                logger.info("✅ Found card with button")
                break
            except:
                continue
        
        if not first_card:
            logger.error("❌ No card with button found")

            return
        
        # Add item first, then remove
        add_to_cart_btn = first_card.find_element(By.TAG_NAME, "button")
        add_to_cart_btn.click()
        logger.info("✅ Added item to cart first")
        
        # Wait for quantity controls to appear
        time.sleep(3)
        
        # Remove item
        remove_btn = first_card.find_element(By.CSS_SELECTOR, "button:has(svg.lucide-trash2)")
        remove_btn.click()
        logger.info("✅ Clicked remove button")
        
        # Wait for cart to update
        time.sleep(3)
        
        logger.info("🎯 Remove item test completed!")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        try:
            logger.info("📸 Error")
        except:
            pass
        raise

def test_update_quantity(driver, app_url, creds):
    """Test update item quantity in cart."""
    logger.info("=== TEST: UPDATE ITEM QUANTITY ===")
    
    try:
        # Login
        login_page = LoginPage(driver)
        login_page.visit(app_url)
        login_page.login(creds["email"], creds["password"])
        login_page.wait_no_error()
        
        # Verify login
        actual_header = login_page.get_pos_header_text()
        expected_header = "POS System"
        assert actual_header == expected_header, f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
        logger.info("✅ Login successful")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find first product card
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.bg-white")
        logger.info(f"Found {len(product_cards)} product cards")
        
        if len(product_cards) == 0:
            logger.error("❌ No product cards found")
            return
        
        # Find card with button
        first_card = None
        for card in product_cards:
            try:
                button = card.find_element(By.TAG_NAME, "button")
                first_card = card
                logger.info("✅ Found card with button")
                break
            except:
                continue
        
        if not first_card:
            logger.error("❌ No card with button found")
            return
        
        # Add item first
        add_to_cart_btn = first_card.find_element(By.TAG_NAME, "button")
        add_to_cart_btn.click()
        logger.info("✅ Added item to cart first")
        
        # Wait for quantity controls to appear
        time.sleep(3)
        
        # Increase quantity
        increase_btn = first_card.find_element(By.CSS_SELECTOR, "button:has(svg.lucide-plus)")
        increase_btn.click()
        logger.info("✅ Clicked increase button")
        
        # Wait for cart to update
        time.sleep(3)
    
        logger.info("🎯 Update quantity test completed!")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        try:
            logger.info("Errir Increase")
        except:
            pass
        raise


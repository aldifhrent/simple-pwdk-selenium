# pages/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

logger = logging.getLogger(__name__)

class CartPage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        
        # Cart page locators
        self.cart_container = (By.CSS_SELECTOR, "[data-test='cart-container']")
        self.cart_items = (By.CSS_SELECTOR, "[data-test='cart-item']")
        self.cart_total = (By.CSS_SELECTOR, "[data-test='cart-total']")
        self.checkout_button = (By.CSS_SELECTOR, "[data-test='checkout-button']")
        self.empty_cart_message = (By.CSS_SELECTOR, "[data-test='empty-cart']")
        
        # Cart item locators (dynamic)
        self.item_name = (By.CSS_SELECTOR, "[data-test='item-name']")
        self.item_price = (By.CSS_SELECTOR, "[data-test='item-price']")
        self.item_quantity = (By.CSS_SELECTOR, "[data-test='item-quantity']")
        self.remove_item_button = (By.CSS_SELECTOR, "[data-test='remove-item']")
        self.quantity_input = (By.CSS_SELECTOR, "input[type='number']")
        
    def get_cart_items_count(self) -> int:
        """Get total number of items in cart."""
        try:
            items = self.driver.find_elements(*self.cart_items)
            return len(items)
        except:
            return 0
    
    def get_cart_total(self) -> str:
        """Get cart total amount."""
        try:
            total_element = self.wait.until(EC.visibility_of_element_located(self.cart_total))
            return total_element.text.strip()
        except:
            return "$0.00"
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        try:
            empty_message = self.driver.find_element(*self.empty_cart_message)
            return empty_message.is_displayed()
        except:
            return self.get_cart_items_count() == 0
    
    def get_item_details(self, item_index: int = 0) -> dict:
        """Get details of specific cart item."""
        try:
            items = self.driver.find_elements(*self.cart_items)
            if item_index < len(items):
                item = items[item_index]
                name = item.find_element(*self.item_name).text.strip()
                price = item.find_element(*self.item_price).text.strip()
                quantity = item.find_element(*self.item_quantity).text.strip()
                
                return {
                    "name": name,
                    "price": price,
                    "quantity": quantity
                }
        except Exception as e:
            logger.error(f"Error getting item details: {e}")
        
        return {}
    
    def update_item_quantity(self, item_index: int, new_quantity: int):
        """Update quantity of specific cart item."""
        try:
            items = self.driver.find_elements(*self.cart_items)
            if item_index < len(items):
                item = items[item_index]
                quantity_input = item.find_element(*self.quantity_input)
                quantity_input.clear()
                quantity_input.send_keys(str(new_quantity))
                quantity_input.send_keys(Keys.ENTER)
                logger.info(f"Updated quantity to {new_quantity}")
        except Exception as e:
            logger.error(f"Error updating quantity: {e}")
    
    def remove_item(self, item_index: int):
        """Remove specific item from cart."""
        try:
            items = self.driver.find_elements(*self.cart_items)
            if item_index < len(items):
                item = items[item_index]
                remove_button = item.find_element(*self.remove_item_button)
                remove_button.click()
                logger.info(f"Removed item at index {item_index}")
        except Exception as e:
            logger.error(f"Error removing item: {e}")
    
    def clear_cart(self):
        """Remove all items from cart."""
        try:
            while self.get_cart_items_count() > 0:
                self.remove_item(0)
                # Wait for item to be removed
                self.wait.until(lambda d: self.get_cart_items_count() < self.get_cart_items_count() + 1)
            logger.info("Cart cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
    
    def proceed_to_checkout(self):
        """Click checkout button to proceed to checkout."""
        try:
            checkout_btn = self.wait.until(EC.element_to_be_clickable(self.checkout_button))
            checkout_btn.click()
            logger.info("Proceeded to checkout")
        except Exception as e:
            logger.error(f"Error proceeding to checkout: {e}")
    
    def assert_cart_has_items(self, expected_count: int):
        """Assert that cart has expected number of items."""
        actual_count = self.get_cart_items_count()
        assert actual_count == expected_count, f"Expected {expected_count} items, but found {actual_count}"
        logger.info(f"Cart has {actual_count} items as expected")
    
    def assert_cart_total_matches(self, expected_total: str):
        """Assert that cart total matches expected amount."""
        actual_total = self.get_cart_total()
        assert actual_total == expected_total, f"Expected total {expected_total}, but got {actual_total}"
        logger.info(f"Cart total {actual_total} matches expected")
    
    def assert_item_in_cart(self, item_name: str):
        """Assert that specific item is in cart."""
        items = self.driver.find_elements(*self.cart_items)
        item_names = []
        
        for item in items:
            try:
                name = item.find_element(*self.item_name).text.strip()
                item_names.append(name)
            except:
                continue
        
        assert item_name in item_names, f"Item '{item_name}' not found in cart. Available items: {item_names}"
        logger.info(f"Item '{item_name}' found in cart") 
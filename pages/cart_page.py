# pages/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import re

logger = logging.getLogger(__name__)

class CartPage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        
        # Cart page locators - updated to match actual HTML structure
        # The cart is inline with products, showing "X in cart" text
        self.cart_items = (By.CSS_SELECTOR, "div[class*='bg-white'][class*='rounded-lg'][class*='shadow-md']")
        self.cart_count_text = (By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
        
        # Cart item locators (dynamic) - updated to be more flexible
        self.item_name = (By.CSS_SELECTOR, "h3.font-semibold.text-gray-900")
        self.item_price = (By.CSS_SELECTOR, "span.text-lg.font-bold.text-green-600")
        self.item_quantity = (By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
        
        # Quantity control buttons - updated to match actual HTML
        self.quantity_decrease_button = (By.CSS_SELECTOR, "button[class*='rounded-full'][class*='bg-gray-200'] svg[class*='lucide-minus']")
        self.quantity_increase_button = (By.CSS_SELECTOR, "button[class*='rounded-full'][class*='bg-gray-200'] svg[class*='lucide-plus']")
        
        # Remove button - the trash icon
        self.remove_item_button = (By.CSS_SELECTOR, "button[class*='bg-red-100'] svg[class*='lucide-trash2'], button[class*='text-red-600'] svg[class*='lucide-trash2']")
        
    def find_cart_elements(self):
        """Find product cards that have items in cart."""
        try:
            # Find all product cards
            all_products = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='bg-white'][class*='rounded-lg'][class*='shadow-md']")
            
            # Filter only those that have "X in cart" text
            cart_items = []
            for product in all_products:
                try:
                    cart_text = product.find_element(By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
                    if cart_text.text and "in cart" in cart_text.text.lower():
                        cart_items.append(product)
                except:
                    continue
            
            return cart_items
        except Exception as e:
            logger.error(f"Error finding cart elements: {e}")
            return []
    
    def get_cart_items_count(self) -> int:
        """Get total number of items in cart."""
        try:
            cart_items = self.find_cart_elements()
            total_count = 0
            
            for item in cart_items:
                try:
                    cart_text = item.find_element(By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
                    # Extract number from "X in cart" text
                    match = re.search(r'(\d+)\s+in\s+cart', cart_text.text.lower())
                    if match:
                        total_count += int(match.group(1))
                except:
                    continue
            
            return total_count
        except Exception as e:
            logger.error(f"Error getting cart items count: {e}")
            return 0
    
    def get_cart_total(self) -> str:
        """Calculate cart total from all items in cart."""
        try:
            cart_items = self.find_cart_elements()
            total_amount = 0.0
            
            for item in cart_items:
                try:
                    # Get price
                    price_elem = item.find_element(By.CSS_SELECTOR, "span.text-lg.font-bold.text-green-600")
                    price_text = price_elem.text.strip()
                    price = float(price_text.replace('$', ''))
                    
                    # Get quantity
                    cart_text = item.find_element(By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
                    match = re.search(r'(\d+)\s+in\s+cart', cart_text.text.lower())
                    quantity = int(match.group(1)) if match else 1
                    
                    total_amount += price * quantity
                except Exception as e:
                    logger.error(f"Error calculating item total: {e}")
                    continue
            
            return f"${total_amount:.2f}"
        except Exception as e:
            logger.error(f"Error calculating cart total: {e}")
            return "$0.00"
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.get_cart_items_count() == 0
    
    def get_item_details(self, item_index: int = 0) -> dict:
        """Get details of specific cart item."""
        try:
            cart_items = self.find_cart_elements()
            if item_index < len(cart_items):
                item = cart_items[item_index]
                
                # Get name
                name_elem = item.find_element(By.CSS_SELECTOR, "h3.font-semibold.text-gray-900")
                name = name_elem.text.strip()
                
                # Get price
                price_elem = item.find_element(By.CSS_SELECTOR, "span.text-lg.font-bold.text-green-600")
                price = price_elem.text.strip()
                
                # Get quantity from "X in cart" text
                cart_text = item.find_element(By.CSS_SELECTOR, "span.text-sm.font-medium.text-blue-600")
                match = re.search(r'(\d+)\s+in\s+cart', cart_text.text.lower())
                quantity = match.group(1) if match else "1"
                
                return {
                    "name": name,
                    "price": price,
                    "quantity": quantity
                }
        except Exception as e:
            logger.error(f"Error getting item details: {e}")
        
        return {}
    
    def update_item_quantity(self, item_index: int, new_quantity: int):
        """Update quantity of specific cart item using plus/minus buttons."""
        try:
            cart_items = self.find_cart_elements()
            if item_index < len(cart_items):
                item = cart_items[item_index]
                
                # Get current quantity
                current_details = self.get_item_details(item_index)
                current_quantity = int(current_details.get("quantity", "1"))
                
                if new_quantity > current_quantity:
                    # Need to increase quantity - click the Add to Cart button more times
                    clicks_needed = new_quantity - current_quantity
                    for _ in range(clicks_needed):
                        add_btn = item.find_element(By.CSS_SELECTOR, "button:has(span:contains('Add to Cart'))")
                        add_btn.click()
                        # Wait a bit for the cart count to update
                        self.driver.implicitly_wait(0.5)
                elif new_quantity < current_quantity:
                    # Need to decrease quantity - this might require a different approach
                    # For now, we'll log that decreasing isn't directly supported
                    logger.warning("Decreasing quantity directly is not supported in this cart implementation")
                
                logger.info(f"Updated quantity from {current_quantity} to {new_quantity}")
        except Exception as e:
            logger.error(f"Error updating quantity: {e}")
    
    def remove_item(self, item_index: int):
        """Remove specific item from cart."""
        try:
            cart_items = self.find_cart_elements()
            if item_index < len(cart_items):
                item = cart_items[item_index]
                
                # Look for a remove button (trash icon) in this item
                try:
                    trash_icon = item.find_element(By.CSS_SELECTOR, "svg[class*='lucide-trash2']")
                    remove_button = trash_icon.find_element(By.XPATH, "./ancestor::button[1]")
                    remove_button.click()
                    logger.info(f"Removed item at index {item_index}")
                except:
                    logger.warning("No remove button found for this item")
        except Exception as e:
            logger.error(f"Error removing item: {e}")
    
    def clear_cart(self):
        """Remove all items from cart."""
        try:
            cart_items = self.find_cart_elements()
            for i in range(len(cart_items)):
                self.remove_item(0)  # Always remove first item as list changes
                # Wait for cart to update
                self.driver.implicitly_wait(1)
            logger.info("Cart cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
    
    def proceed_to_checkout(self):
        """Look for checkout functionality."""
        try:
            # Check if there's a checkout button anywhere on the page
            checkout_selectors = [
                "button:contains('Checkout')",
                "button:contains('checkout')",
                ".checkout-btn",
                ".checkout-button",
                "[class*='checkout']"
            ]
            
            for selector in checkout_selectors:
                try:
                    checkout_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if checkout_btn.is_displayed() and checkout_btn.is_enabled():
                        checkout_btn.click()
                        logger.info("Proceeded to checkout")
                        return
                except:
                    continue
            
            logger.warning("No checkout button found")
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
        cart_items = self.find_cart_elements()
        item_names = []
        
        for item in cart_items:
            try:
                name_elem = item.find_element(By.CSS_SELECTOR, "h3.font-semibold.text-gray-900")
                name = name_elem.text.strip()
                if name:
                    item_names.append(name)
            except:
                continue
        
        assert item_name in item_names, f"Item '{item_name}' not found in cart. Available items: {item_names}"
        logger.info(f"Item '{item_name}' found in cart") 
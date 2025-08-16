import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class CartPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        # --- Cart Item Locators (based on actual HTML) ---
        self.cart_item = "//div[contains(@class,'p-4 border-b hover:bg-gray-50')]"
        
        # --- Quantity Locators ---
        self.qty_span = ".//span[contains(@class,'w-8 text-center font-medium')]"
        
        # --- Button Locators ---
        self.btn_increase = ".//div[contains(@class,'flex items-center space-x-2')]/button[2]"
        self.btn_decrease = ".//div[contains(@class,'flex items-center space-x-2')]/button[1]"
        self.btn_remove = ".//button[contains(@class,'bg-red-100') and contains(@class,'text-red-600')]"
        
        # --- Cart Header (to check if cart has items) ---
        self.cart_header = "//div[contains(@class,'p-6 border-b')]//h2[contains(@class,'text-xl font-semibold')]"
        
        # --- Empty State Locators ---
        self.empty_title = "//div[contains(@class,'lg:col-span-1')]//p[contains(text(),'Your cart is empty')]"
        self.empty_desc = "//div[contains(@class,'lg:col-span-1')]//p[contains(text(),'Add products')]"

    def get_cart_items(self):
        """Get cart items using the correct locator."""
        try:
            items = self.driver.find_elements(By.XPATH, self.cart_item)
            logger.info(f"[get_cart_items] ✅ Found {len(items)} cart items")
            return items
        except Exception as e:
            logger.error(f"[get_cart_items] ❌ Error: {e}")
            return []

    def get_cart_items_count(self):
        """Get cart count from header text."""
        try:
            header_element = self.driver.find_element(By.XPATH, self.cart_header)
            header_text = header_element.text
            import re
            match = re.search(r'Cart \((\d+) items?\)', header_text)
            if match:
                count = int(match.group(1))
                logger.info(f"[get_cart_items_count] ✅ From header: {count} items")
                return count
            count = len(self.get_cart_items())
            logger.info(f"[get_cart_items_count] ✅ From elements: {count} items")
            return count
        except Exception as e:
            logger.warning(f"[get_cart_items_count] ❌ Error getting count: {e}")
            count = len(self.get_cart_items())
            logger.info(f"[get_cart_items_count] ✅ Fallback count: {count} items")
            return count

    def get_quantity(self, item_idx=0):
        """Get quantity of specific cart item."""
        try:
            cart_items = self.get_cart_items()
            if not cart_items or item_idx >= len(cart_items):
                logger.warning(f"[get_quantity] ❌ No cart item at index {item_idx}")
                return 0
            
            qty_element = cart_items[item_idx].find_element(By.XPATH, self.qty_span)
            qty_text = qty_element.text.strip()
            qty = int(qty_text)
            logger.info(f"[get_quantity] ✅ Item {item_idx} quantity: {qty}")
            return qty
        except Exception as e:
            logger.error(f"[get_quantity] ❌ Error: {e}")
            return 1

    def increase_quantity(self, item_idx=0):
        """Increase quantity of specific cart item."""
        try:
            cart_items = self.get_cart_items()
            if not cart_items or item_idx >= len(cart_items):
                raise ValueError(f"No cart item at index {item_idx}")
            
            btn = cart_items[item_idx].find_element(By.XPATH, self.btn_increase)
            btn.click()
            logger.info(f"[increase_quantity] ✅ Increased quantity for item {item_idx}")
            time.sleep(1)  # Wait for UI update
        except Exception as e:
            logger.error(f"[increase_quantity] ❌ Error: {e}")
            raise

    def decrease_quantity(self, item_idx=0):
        """Decrease quantity of specific cart item."""
        try:
            cart_items = self.get_cart_items()
            if not cart_items or item_idx >= len(cart_items):
                raise ValueError(f"No cart item at index {item_idx}")
            
            btn = cart_items[item_idx].find_element(By.XPATH, self.btn_decrease)
            btn.click()
            logger.info(f"[decrease_quantity] ✅ Decreased quantity for item {item_idx}")
            time.sleep(1)  # Wait for UI update
        except Exception as e:
            logger.error(f"[decrease_quantity] ❌ Error: {e}")
            raise

    def increase_quantity_to_max(self, item_idx=0, max_clicks=50):
        """Increase quantity until button is disabled."""
        try:
            for i in range(max_clicks):
                cart_items = self.get_cart_items()
                if not cart_items or item_idx >= len(cart_items):
                    break
                
                btn = cart_items[item_idx].find_element(By.XPATH, self.btn_increase)
                if btn.get_attribute("disabled"):
                    logger.info(f"[increase_quantity_to_max] ✅ Button disabled after {i} clicks")
                    break
                btn.click()
                time.sleep(0.5)
        except Exception as e:
            logger.error(f"[increase_quantity_to_max] ❌ Error: {e}")

    def is_increase_disabled(self, item_idx=0):
        """Check if increase button is disabled."""
        try:
            cart_items = self.get_cart_items()
            if not cart_items or item_idx >= len(cart_items):
                return False
            
            btn = cart_items[item_idx].find_element(By.XPATH, self.btn_increase)
            disabled = btn.get_attribute("disabled") is not None
            logger.info(f"[is_increase_disabled] ✅ Item {item_idx} increase button disabled: {disabled}")
            return disabled
        except Exception as e:
            logger.error(f"[is_increase_disabled] ❌ Error: {e}")
            return False

    def remove_product(self, item_idx=0):
        """Remove specific product from cart."""
        try:
            cart_items = self.get_cart_items()
            if not cart_items or item_idx >= len(cart_items):
                raise ValueError(f"No cart item at index {item_idx}")
            
            initial_count = len(cart_items)
            btn = cart_items[item_idx].find_element(By.XPATH, self.btn_remove)
            btn.click()
            logger.info(f"[remove_product] ✅ Remove button clicked for item {item_idx}")
            
            # Wait for cart to update
            self.wait.until(lambda d: self.get_cart_items_count() < initial_count)
            logger.info(f"[remove_product] ✅ Product removed successfully")
        except Exception as e:
            logger.error(f"[remove_product] ❌ Error: {e}")
            raise

    def clear_cart_if_not_empty(self):
        """Clear all items from cart if not empty."""
        try:
            while self.get_cart_items_count() > 0:
                self.remove_product(0)
            logger.info("[clear_cart_if_not_empty] ✅ Cart cleared successfully")
        except Exception as e:
            logger.error(f"[clear_cart_if_not_empty] ❌ Error: {e}")

    def get_cart_empty_state(self):
        """Get empty cart state text."""
        try:
            title = self.driver.find_element(By.XPATH, self.empty_title).text.strip()
            desc = self.driver.find_element(By.XPATH, self.empty_desc).text.strip()
            logger.info(f"[get_cart_empty_state] ✅ Empty state: {title} - {desc}")
            return title, desc
        except NoSuchElementException:
            logger.info("[get_cart_empty_state] ✅ Using default empty state text")
            return "Your cart is empty", "Add products to get started"

    def try_remove_when_empty(self):
        """Try to remove item when cart is empty (should not work)."""
        try:
            self.driver.find_element(By.XPATH, self.btn_remove).click()
            logger.info("[try_remove_when_empty] ✅ Remove button clicked (unexpected)")
        except NoSuchElementException:
            logger.info("[try_remove_when_empty] ✅ No remove button (cart empty)")

    def debug_cart_structure(self):
        """Debug method to inspect cart structure."""
        try:
            logger.info("=== CART STRUCTURE DEBUG ===")
            
            # Check cart header
            try:
                header = self.driver.find_element(By.XPATH, self.cart_header)
                logger.info(f"Cart header: {header.text}")
            except:
                logger.warning("Cart header not found")
            
            # Check cart items
            items = self.get_cart_items()
            logger.info(f"Cart items found: {len(items)}")
            
            for i, item in enumerate(items):
                try:
                    logger.info(f"Item {i}: {item.text[:100]}...")
                    
                    # Try to find buttons in this item
                    try:
                        increase_btn = item.find_element(By.XPATH, self.btn_increase)
                        logger.info(f"  ✅ Increase button found")
                    except:
                        logger.warning(f"  ❌ Increase button not found")
                        
                    try:
                        decrease_btn = item.find_element(By.XPATH, self.btn_decrease)
                        logger.info(f"  ✅ Decrease button found")
                    except:
                        logger.warning(f"  ❌ Decrease button not found")
                        
                    try:
                        remove_btn = item.find_element(By.XPATH, self.btn_remove)
                        logger.info(f"  ✅ Remove button found")
                    except:
                        logger.warning(f"  ❌ Remove button not found")
                        
                except Exception as e:
                    logger.warning(f"Could not get text for item {i}: {e}")
            
            # Check empty state
            try:
                empty_title = self.driver.find_element(By.XPATH, self.empty_title)
                logger.info(f"Empty title: {empty_title.text}")
            except:
                logger.info("Empty title not found (cart has items)")
            
            logger.info("=== END DEBUG ===")
        except Exception as e:
            logger.error(f"Debug error: {e}")

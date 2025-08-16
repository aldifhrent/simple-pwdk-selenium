from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class ProductsPage:
    SEARCH_BOX = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    CATEGORY_DROPDOWN = (By.CSS_SELECTOR, "select.px-4.py-2.border")
    NO_PRODUCTS_MSG = (By.XPATH, "//p[normalize-space()='No products found']")
    CART_EMPTY_MSG = (By.XPATH, "//div[contains(@class,'lg:col-span-1')]//p[normalize-space()='Your cart is empty']")
    PRODUCT_CARD = "//h3[normalize-space()]"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_no_products_found(self):
        try:
            return self.driver.find_element(*self.NO_PRODUCTS_MSG).is_displayed()
        except NoSuchElementException:
            return False

    def assert_product_visible(self, product_name):
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//h3[normalize-space()='{product_name}']"))
            )
        except TimeoutException:
            raise AssertionError(f"Produk '{product_name}' tidak ditemukan di hasil pencarian")

    def find_product_card(self, product_name):
        return self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//h3[normalize-space()='{product_name}']/ancestor::div[contains(@class,'shadow-md')]")
            )
        )

    def search_product(self, product_name):
        logger.info(f"[search_product] Mencari produk: {product_name}")
        
        # Find and clear search box
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(product_name)
        logger.info(f"[search_product] Input '{product_name}' ke search box")

        # Wait for search results
        try:
            # Wait for either product cards or no products message
            self.wait.until(
                lambda d: len(d.find_elements(By.XPATH, self.PRODUCT_CARD)) > 0 or 
                          self.is_no_products_found()
            )
            
            # Check if products found
            products_found = len(self.driver.find_elements(By.XPATH, self.PRODUCT_CARD))
            if products_found > 0:
                logger.info(f"[search_product] ✅ Ditemukan {products_found} produk")
            else:
                logger.warning(f"[search_product] ⚠️ Tidak ada produk ditemukan")
                
        except TimeoutException:
            logger.error(f"[search_product] ❌ Timeout: Hasil pencarian tidak muncul")
            raise AssertionError(f"Hasil pencarian untuk '{product_name}' tidak muncul dalam waktu tunggu")

    def add_to_cart(self, product_name):
        logger.info(f"[add_to_cart] Menambahkan '{product_name}' ke cart")
        
        try:
            # Find product card
            card = self.find_product_card(product_name)
            logger.info(f"[add_to_cart] ✅ Product card ditemukan")
            
            # Find Add to Cart button
            add_btn = card.find_element(By.XPATH, ".//button[.//span[normalize-space()='Add to Cart']]")
            logger.info(f"[add_to_cart] ✅ Add to Cart button ditemukan")
            
            # Click button
            add_btn.click()
            logger.info(f"[add_to_cart] ✅ Add to Cart button diklik")
            
            # Wait a bit for UI to update
            import time
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"[add_to_cart] ❌ Error: {str(e)}")
            raise AssertionError(f"Gagal menambahkan '{product_name}' ke cart: {str(e)}")

    def filter_by_category(self, category_name):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.CATEGORY_DROPDOWN))
        Select(dropdown).select_by_visible_text(category_name)

    def is_product_in_cart(self, product_name):
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//div[contains(@class,'lg:col-span-1')]//h3[normalize-space()='{product_name}']")
                )
            )
            return True
        except TimeoutException:
            return False

    def is_add_to_cart_disabled(self, product_name):
        card = self.find_product_card(product_name)
        btn = card.find_element(By.XPATH, ".//button[.//span[normalize-space()='Add to Cart']]")
        return not btn.is_enabled()

    def has_add_to_cart_button(self):
        return len(self.driver.find_elements(By.XPATH, "//button[.//span[normalize-space()='Add to Cart']]")) > 0

    def is_cart_empty(self):
        try:
            return self.driver.find_element(*self.CART_EMPTY_MSG).is_displayed()
        except NoSuchElementException:
            return False

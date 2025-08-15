from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


class PosPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_no_products_found(self):
        try:
            msg = self.driver.find_element(
                By.XPATH, "//p[normalize-space()='No products found']"
            )
            return msg.is_displayed()
        except:
            return False

    def assert_product_visible(self, product_name):
        """Pastikan produk terlihat di hasil pencarian."""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//h3[normalize-space()='{product_name}']")
                )
            )
        except:
            raise AssertionError(
                f"Produk '{product_name}' tidak ditemukan di hasil pencarian"
            )

    def select_product(self, product_name):
        """Klik tombol Add to Cart dari produk yang dicari."""
        self.add_to_cart(product_name)

    def find_product_card(self, product_name):
        """Temukan elemen card produk berdasarkan nama."""
        return self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//h3[normalize-space()='{product_name}']/ancestor::div[contains(@class,'shadow-md')]",
                )
            )
        )

    def search_product(self, product_name):
        search_box = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Search products...']")
            )
        )
        search_box.clear()
        search_box.send_keys(product_name)

    def add_to_cart(self, product_name):
        card = self.find_product_card(product_name)
        add_btn = card.find_element(
            By.XPATH, ".//button[.//span[normalize-space()='Add to Cart']]"
        )
        add_btn.click()

    def filter_by_category(self, category_name):
        """Pilih kategori produk dari dropdown"""
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select.px-4.py-2.border"))
        )
        select = Select(dropdown)
        select.select_by_visible_text(category_name)

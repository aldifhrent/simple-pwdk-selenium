from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import re
class PosPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    def click_button_by_text(self, text):
        btn = self.wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//button[contains(normalize-space(), '{text}')]"
        )))
        btn.click()

    def assert_product_visible(self, product_name):
        """Pastikan produk terlihat di hasil pencarian."""
        try:
            self.wait.until(EC.visibility_of_element_located((
            By.XPATH, f"//h3[normalize-space()='{product_name}']"
            )))
        except:
            raise AssertionError(f"Produk '{product_name}' tidak ditemukan di hasil pencarian")

    def select_product(self, product_name):
        """Klik tombol Add to Cart dari produk yang dicari."""
        self.add_to_cart(product_name)

    # === Helper umum ===
    def find_product_card(self, product_name):
        """Temukan elemen card produk berdasarkan nama."""
        return self.wait.until(EC.presence_of_element_located((
            By.XPATH, f"//h3[normalize-space()='{product_name}']/ancestor::div[contains(@class,'shadow-md')]"
        )))

    # === Fitur POS ===
    def search_product(self, product_name):
        search_box = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "input[placeholder='Search products...']"
        )))
        search_box.clear()
        search_box.send_keys(product_name)

    def add_to_cart(self, product_name):
        card = self.find_product_card(product_name)
        add_btn = card.find_element(By.XPATH, ".//button[.//span[normalize-space()='Add to Cart']]")
        add_btn.click()

    def increase_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        plus_btn = card.find_element(By.CSS_SELECTOR, "button svg.lucide-plus")
        plus_btn.click()

    def decrease_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        minus_btn = card.find_element(By.CSS_SELECTOR, "button svg.lucide-minus")
        minus_btn.click()

    def remove_product(self, product_name):
        card = self.find_product_in_cart(product_name)
        remove_btn = card.find_element(By.CSS_SELECTOR, "button.bg-red-100")
        remove_btn.click()

    def find_product_in_cart(self, product_name):
        """Cari produk di dalam cart."""
        return self.wait.until(EC.presence_of_element_located((
            By.XPATH, f"//div[contains(@class,'max-h-96')]//h3[normalize-space()='{product_name}']/ancestor::div[contains(@class,'flex items-center')]"
        )))

    def get_cart_items_count(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, ".max-h-96.overflow-y-auto > div")
        return len(items)

    def checkout(self):
        self.click_button_by_text("Checkout")

    def fill_customer_info(self, name, email):
        name_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "input[placeholder='Enter customer name']"
        )))
        name_input.clear()
        name_input.send_keys(name)

        email_input = self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "input[placeholder='Enter customer email']"
        )))
        email_input.clear()
        email_input.send_keys(email)

    def select_payment_method(self, method="Cash"):
        method_btn = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//button[.//span[normalize-space()='{method}']]"
        )))
        method_btn.click()

    def complete_payment(self):
        self.click_button_by_text("Complete Payment")

    def complete_transaction(self):
        self.click_button_by_text("Complete Transaction")

    def get_transaction_alert_and_id(self):
        """Ambil teks alert dan TXID dari alert browser."""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text.strip()
            alert.accept()
        except Exception:
            return None, None

        match = re.search(r"TXN-\d{8}-\d{6}", alert_text)
        txid = match.group(0) if match else None
        return alert_text, txid

    def filter_by_category(self, category_name):
        """Pilih kategori produk dari dropdown"""
        dropdown = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "select.px-4.py-2.border"
        )))
        select = Select(dropdown)
        select.select_by_visible_text(category_name)

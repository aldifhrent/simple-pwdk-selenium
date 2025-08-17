import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.helper import click_button_by_text
import re

logger = logging.getLogger(__name__)

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Lokator absolute cart (item pertama)
        self.cart_item = "//*[@id='root']/div/main/div/div[2]/div/div[2]/div/div[1]"
        self.qty_span = f"{self.cart_item}/div[2]/div/span"
        self.btn_increase = f"{self.cart_item}/div[2]/div/button[2]"
        self.btn_decrease = f"{self.cart_item}/div[2]/div/button[1]"
        self.btn_remove = f"{self.cart_item}/div[2]/button"

        # Empty state
        self.empty_title = "//*[@id='root']/div/main/div/div[2]/div/div/h2"
        self.empty_desc = "//*[@id='root']/div/main/div/div[2]/div/div/p"

    # =========================
    # Cart Item Handling
    # =========================
    def find_product_in_cart(self):
        """Cek apakah ada produk di cart (item pertama)."""
        try:
            self.driver.find_element(By.XPATH, self.cart_item)
            return True
        except NoSuchElementException:
            return False

    def get_cart_items_count(self):
        """Hitung jumlah item di cart (pakai div.cart-item)."""
        items = self.driver.find_elements(By.XPATH, "//*[@id='root']/div/main/div/div[2]/div/div[2]/div/div")
        return len(items)

    def get_cart_items(self):
        """Return semua elemen item cart."""
        return self.driver.find_elements(By.XPATH, "//*[@id='root']/div/main/div/div[2]/div/div[2]/div/div")

    # =========================
    # Quantity Handling
    # =========================
    def get_quantity(self):
        """Ambil quantity produk pertama di cart."""
        try:
            qty_text = self.driver.find_element(By.XPATH, self.qty_span).text.strip()
            qty = int(qty_text)
            logger.info(f"[get_quantity] ✅ Quantity saat ini: {qty}")
            return qty
        except Exception as e:
            logger.error(f"[get_quantity] ❌ Error: {e}")
            return 0

    def increase_quantity(self):
        """Klik tombol + sekali."""
        btn = self.driver.find_element(By.XPATH, self.btn_increase)
        btn.click()
        time.sleep(0.3)

    def decrease_quantity(self):
        """Klik tombol - sekali."""
        btn = self.driver.find_element(By.XPATH, self.btn_decrease)
        btn.click()
        time.sleep(0.3)

    def increase_quantity_to_max(self, max_clicks=50):
        """Klik tombol + sampai disabled."""
        qty = self.get_quantity()
        for _ in range(max_clicks):
            btn = self.driver.find_element(By.XPATH, self.btn_increase)
            if btn.get_attribute("disabled"):
                logger.info("[increase_quantity_to_max] ✅ Tombol + sudah disabled")
                break
            btn.click()
            time.sleep(0.3)
            qty = self.get_quantity()
        return qty

    def decrease_quantity_to_zero(self):
        """Klik tombol - sampai produk hilang dari cart."""
        qty = self.get_quantity()
        logger.info(f"[decrease_quantity_to_zero] Mulai decrease dari qty={qty}")
        while self.find_product_in_cart():
            btn = self.driver.find_element(By.XPATH, self.btn_decrease)
            btn.click()
            time.sleep(0.2)
        logger.info("[decrease_quantity_to_zero] ✅ Produk sudah hilang dari cart")

    def is_increase_disabled(self):
        """Cek apakah tombol + disabled."""
        try:
            btn = self.driver.find_element(By.XPATH, self.btn_increase)
            disabled = btn.get_attribute("disabled") is not None
            logger.info(f"[is_increase_disabled] ✅ Disabled: {disabled}")
            return disabled
        except Exception as e:
            logger.error(f"[is_increase_disabled] ❌ Error: {e}")
            return False

    # =========================
    # Remove & Empty State
    # =========================
    def remove_product(self):
        """Klik tombol remove (trash)"""
        try:
            self.driver.find_element(By.XPATH, self.btn_remove).click()
            logger.info("[remove_product] ✅ Produk dihapus dari cart")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"[remove_product] ❌ Error: {e}")

    def clear_cart_if_not_empty(self):
        """Hapus semua produk di cart kalau ada."""
        while self.find_product_in_cart():
            self.remove_product()
            time.sleep(0.5)
        logger.info("[clear_cart_if_not_empty] ✅ Cart sudah kosong")
    
    def get_cart_empty_state(self):
        """Ambil teks empty state di cart (misal: 'Your cart is empty')."""
        try:
            text = self.driver.find_element(By.CSS_SELECTOR, "p.text-gray-500").text.strip()
            logger.info(f"[get_cart_empty_state] 📝 Empty state: '{text}'")
            return text
        except Exception as e:
            logger.error(f"[get_cart_empty_state] ❌ Error: {e}")
            return ""


    def try_remove_when_empty(self):
        """Coba klik remove meskipun cart kosong (negative test)."""
        try:
            self.driver.find_element(By.XPATH, self.btn_remove).click()
            logger.warning("[try_remove_when_empty] ⚠️ Berhasil klik remove padahal cart kosong!")
        except NoSuchElementException:
            logger.info("[try_remove_when_empty] ✅ Tidak ada tombol remove (cart kosong)")


    # Checkout

    def checkout(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Checkout')]"))
        ).click()

    def fill_customer_info(self, name, email):
        name_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Enter customer name']")
            )
        )
        name_input.clear()
        name_input.send_keys(name)

        email_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Enter customer email']")
            )
        )
        email_input.clear()
        email_input.send_keys(email)

    def select_payment_method(self, method="Cash"):
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[.//span[normalize-space()='{method}']]")
            )
        ).click()

    def complete_transaction(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Complete Transaction')]"))
        ).click()

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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from util.helper import click_button_by_text


class CartPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =============== BASIC ACTIONS ===============
    def get_cart_items_count(self):
        """Hitung jumlah item di cart"""
        items = self.driver.find_elements(
            By.CSS_SELECTOR, ".max-h-96.overflow-y-auto > div"
        )
        return len(items)

    def get_first_cart_item_name(self):
        """Ambil nama produk pertama di cart"""
        first_item = self.driver.find_element(
            By.CSS_SELECTOR, ".max-h-96.overflow-y-auto > div:first-child h3"
        )
        return first_item.text

    def remove_product(self, product_name):
        """Remove produk berdasarkan nama"""
        card = self.find_product_in_cart(product_name)
        remove_btn = card.find_element(By.CSS_SELECTOR, "button.bg-red-100")
        remove_btn.click()

    def find_product_in_cart(self, product_name):
        """Cari produk di dalam cart"""
        return self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[contains(@class,'max-h-96')]//h3[normalize-space()='{product_name}']/ancestor::div[contains(@class,'flex items-center')]",
                )
            )
        )

    # =============== CART MANAGEMENT ===============
    def clear_cart_if_not_empty(self):
        """Hapus semua item di cart jika ada"""
        try:
            while self.get_cart_items_count() > 0:
                first_item = self.get_first_cart_item_name()
                self.remove_product(first_item)
        except:
            pass

    def get_cart_empty_state(self):
        """Ambil teks judul dan deskripsi jika cart kosong"""
        try:
            title = self.driver.find_element(
                By.XPATH, "//p[contains(normalize-space(),'Your cart is empty')]"
            ).text.strip()
        except:
            title = None

        try:
            desc = self.driver.find_element(
                By.XPATH,
                "//p[contains(normalize-space(),'Add products to get started')]",
            ).text.strip()
        except:
            desc = None

        return title, desc

    # =============== QUANTITY HANDLING ===============
    def increase_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        plus_btn = card.find_element(By.CSS_SELECTOR, "button svg.lucide-plus")
        plus_btn.click()

    def decrease_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        minus_btn = card.find_element(By.CSS_SELECTOR, "button svg.lucide-minus")
        minus_btn.click()

    def increase_quantity_to_max(self, product_name):
        """Klik tombol '+' sampai disabled"""
        while True:
            try:
                card = self.find_product_in_cart(product_name)
                plus_parent = card.find_element(
                    By.XPATH, ".//svg[contains(@class,'lucide-plus')]/ancestor::button"
                )
                if plus_parent.get_attribute(
                    "disabled"
                ) or "cursor-not-allowed" in plus_parent.get_attribute("class"):
                    break
                plus_parent.click()
            except:
                break

    def is_increase_disabled(self, product_name):
        """Cek apakah tombol '+' disabled"""
        try:
            card = self.find_product_in_cart(product_name)
            plus_parent = card.find_element(
                By.XPATH, ".//svg[contains(@class,'lucide-plus')]/ancestor::button"
            )
            return plus_parent.get_attribute("disabled") is not None
        except:
            return False

    def decrease_quantity_to_zero(self, product_name):
        """Klik tombol '-' sampai item hilang"""
        while self.get_cart_items_count() > 0:
            try:
                self.decrease_quantity(product_name)
            except:
                break

    # =============== NEGATIVE TEST HELPER ===============
    def try_remove_when_empty(self):
        """Coba klik remove jika kosong"""
        try:
            remove_btn = self.driver.find_element(By.CSS_SELECTOR, "button.bg-red-100")
            remove_btn.click()
            return True
        except:
            return False


    def checkout(self):
        click_button_by_text(self.driver, "Checkout")

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
        method_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[.//span[normalize-space()='{method}']]")
            )
        )
        method_btn.click()

    def complete_payment(self):
        click_button_by_text(self.driver, "Complete Payment")

    def complete_transaction(self):
        click_button_by_text(self.driver, "Complete Transaction")

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

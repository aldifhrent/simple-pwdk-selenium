from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from util.helper import click_button_by_text
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"[get_cart_items_count] Jumlah item di cart: {len(items)}")
        return len(items)

    def get_first_cart_item_name(self):
        """Ambil nama produk pertama di cart"""
        first_item = self.driver.find_element(
            By.CSS_SELECTOR, ".max-h-96.overflow-y-auto > div:first-child h3"
        )
        name = first_item.text
        logger.info(f"[get_first_cart_item_name] Produk pertama di cart: {name}")
        return name

    def get_product_quantity_in_cart(self, product_name):
        """Dapatkan quantity produk tertentu di cart"""
        try:
            card = self.find_product_in_cart(product_name)
            # Cari span yang berisi quantity (berdasarkan HTML: <span class="w-8 text-center font-medium">40</span>)
            quantity_span = card.find_element(
                By.XPATH, 
                ".//span[contains(@class,'w-8 text-center font-medium')]"
            )
            quantity = int(quantity_span.text.strip())
            logger.info(f"[get_product_quantity_in_cart] Quantity {product_name}: {quantity}")
            return quantity
        except Exception as e:
            logger.warning(f"[get_product_quantity_in_cart] Tidak bisa mendapatkan quantity untuk {product_name}: {e}")
            return 0

    def remove_product(self, product_name):
        """Remove produk berdasarkan nama"""
        card = self.find_product_in_cart(product_name)
        remove_btn = card.find_element(By.CSS_SELECTOR, "button.bg-red-100")
        remove_btn.click()
        logger.info(f"[remove_product] Produk '{product_name}' dihapus dari cart")

    def find_product_in_cart(self, product_name):
        """Cari produk di dalam cart"""
        logger.info(f"[find_product_in_cart] Mencari '{product_name}' di cart")
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
            logger.info("[clear_cart_if_not_empty] Cart dikosongkan")
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

        logger.info(f"[get_cart_empty_state] title={title}, desc={desc}")
        return title, desc

    # =============== QUANTITY HANDLING ===============
    def increase_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        plus_btn = self._find_increase_button(product_name)
        if plus_btn and plus_btn.is_enabled():
            plus_btn.click()
            logger.info(f"[increase_quantity] Qty '{product_name}' ditambah 1")
        else:
            logger.warning(f"[increase_quantity] Tombol '+' untuk '{product_name}' tidak tersedia atau disabled")

    def decrease_quantity(self, product_name):
        card = self.find_product_in_cart(product_name)
        minus_btn = self._find_decrease_button(product_name)
        if minus_btn and minus_btn.is_enabled():
            minus_btn.click()
            logger.info(f"[decrease_quantity] Qty '{product_name}' dikurangi 1")
        else:
            logger.warning(f"[decrease_quantity] Tombol '-' untuk '{product_name}' tidak tersedia atau disabled")

    def increase_quantity_to_max(self, product_name):
        click_count = 0
        logger.info(f"[increase_quantity_to_max] Mulai klik '+' untuk '{product_name}'")

        while True:
            plus_btn = self._find_increase_button(product_name)

            if not plus_btn:
                logger.warning(f"[increase_quantity_to_max] Tombol '+' tidak ditemukan untuk {product_name}")
                break

            if not plus_btn.is_enabled():
                logger.info(f"[increase_quantity_to_max] Tombol '+' sudah disabled. Total klik: {click_count}")
                break

            plus_btn.click()
            click_count += 1
            logger.info(f"[increase_quantity_to_max] Klik ke-{click_count}")

            # Dapatkan qty sebelum klik
            prev_qty = self.get_product_quantity_in_cart(product_name)

            # Tunggu sampai qty berubah
            self.wait.until(
                lambda d: self.get_product_quantity_in_cart(product_name) != prev_qty
            )


    def _find_increase_button(self, product_name):
        """Temukan tombol + di cart untuk produk tertentu."""
        card = self.find_product_in_cart(product_name)
        try:
            # Ambil semua tombol di dalam container qty (minus & plus)
            buttons = card.find_elements(By.XPATH, ".//button[contains(@class,'rounded-full')]")
            if len(buttons) >= 2:
                plus_btn = buttons[-1]  # Tombol terakhir biasanya tombol +
                logger.info(f"[_find_increase_button] Tombol '+' ditemukan untuk {product_name}")
                return plus_btn
        except Exception as e:
            logger.warning(f"[_find_increase_button] Tombol '+' tidak ditemukan untuk {product_name}: {e}")
            return None

    def _find_decrease_button(self, product_name):
        """Temukan tombol - di cart untuk produk tertentu."""
        card = self.find_product_in_cart(product_name)
        
        # Berdasarkan HTML yang sebenarnya, tombol - ada dalam div dengan class "flex items-center space-x-2"
        try:
            # Cari tombol dengan SVG lucide-minus
            minus_btn = card.find_element(
                By.XPATH, 
                ".//button[.//svg[contains(@class,'lucide-minus')]]"
            )
            logger.info(f"[_find_decrease_button] Tombol '-' ditemukan untuk {product_name}")
            return minus_btn
        except:
            logger.warning(f"[_find_decrease_button] Tombol '-' tidak ditemukan untuk {product_name}")
            return None

    def is_increase_disabled(self, product_name):
        """Cek apakah tombol '+' disabled."""
        plus_btn = self._find_increase_button(product_name)
        if not plus_btn:
            logger.warning(f"[is_increase_disabled] Tombol '+' untuk '{product_name}' tidak ditemukan")
            return True
        
        # Cek atribut disabled dan class yang menunjukkan disabled
        is_disabled = (
            plus_btn.get_attribute("disabled") is not None or
            "disabled:opacity-50" in plus_btn.get_attribute("class") or
            "disabled:cursor-not-allowed" in plus_btn.get_attribute("class")
        )
        
        logger.info(f"[is_increase_disabled] Status tombol '+' untuk '{product_name}': {'disabled' if is_disabled else 'enabled'}")
        return is_disabled

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

    def debug_cart_structure(self, product_name):
        """Debug: tampilkan struktur HTML cart untuk produk tertentu"""
        try:
            card = self.find_product_in_cart(product_name)
            logger.info(f"[debug_cart_structure] Struktur HTML untuk {product_name}:")
            logger.info(f"[debug_cart_structure] Card HTML: {card.get_attribute('outerHTML')}")
            
            # Cari semua button dalam card
            all_buttons = card.find_elements(By.TAG_NAME, "button")
            logger.info(f"[debug_cart_structure] Jumlah button dalam card: {len(all_buttons)}")
            
            for i, btn in enumerate(all_buttons):
                btn_html = btn.get_attribute('outerHTML')
                btn_classes = btn.get_attribute('class')
                btn_aria_label = btn.get_attribute('aria-label')
                logger.info(f"[debug_cart_structure] Button {i+1}: class='{btn_classes}', aria-label='{btn_aria_label}'")
                logger.info(f"[debug_cart_structure] Button {i+1} HTML: {btn_html}")
                
        except Exception as e:
            logger.error(f"[debug_cart_structure] Error: {e}")

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

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CartPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.product_cards_locator = (By.CSS_SELECTOR, "div.p-4")  # card produk
        self.qty_label = (By.CSS_SELECTOR, "span.w-8.text-center.font-medium")

    def add_first_product_to_cart(self):
        """Klik Add to Cart produk pertama lalu tunggu quantity = 1."""
        first_card = self.driver.find_elements(*self.product_cards_locator)[0]
        add_btn = first_card.find_element(By.XPATH, ".//button[.//span[text()='Add to Cart']]")
        add_btn.click()

        # Tunggu tombol hilang
        self.wait.until(EC.staleness_of(add_btn))

        # Tunggu quantity muncul = "1"
        self.wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "span.w-8.text-center.font-medium"), "1"
        ))

    def increase_first_product(self):
        """Klik tombol plus di produk pertama lalu tunggu quantity bertambah."""
        first_card = self.driver.find_elements(*self.product_cards_locator)[0]
        qty_elem = first_card.find_element(*self.qty_label)
        old_qty = int(qty_elem.text)

        plus_btn = first_card.find_element(
            By.XPATH, ".//svg[contains(@class,'lucide-plus')]/ancestor::button"
        )
        plus_btn.click()

        self.wait.until(EC.text_to_be_present_in_element(self.qty_label, str(old_qty + 1)))

    def decrease_first_product(self):
        """Klik tombol minus di produk pertama lalu tunggu quantity berkurang."""
        first_card = self.driver.find_elements(*self.product_cards_locator)[0]
        qty_elem = first_card.find_element(*self.qty_label)
        old_qty = int(qty_elem.text)

        minus_btn = first_card.find_element(
            By.XPATH, ".//svg[contains(@class,'lucide-minus')]/ancestor::button"
        )
        minus_btn.click()

        self.wait.until(EC.text_to_be_present_in_element(self.qty_label, str(old_qty - 1)))

    def remove_first_product(self):
        """Klik tombol remove di produk pertama lalu tunggu card hilang."""
        first_card = self.driver.find_elements(*self.product_cards_locator)[0]
        remove_btn = first_card.find_element(
            By.XPATH, ".//svg[contains(@class,'lucide-trash2')]/ancestor::button"
        )
        remove_btn.click()

        self.wait.until(EC.staleness_of(first_card))

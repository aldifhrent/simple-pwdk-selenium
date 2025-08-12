# pages/products_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    # Search box sesuai snippet
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search products...']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---- Locators berbasis nama produk ----
    def NAME_HEADING(self, name: str):
        # <h3 class="...">Wireless Headphones</h3>
        return (By.XPATH, f"//h3[normalize-space()='{name}']")

    def CARD_BY_NAME(self, name: str):
        # Card root = ancestor <div class="p-4"> terdekat dari <h3>
        return (By.XPATH, f"//h3[normalize-space()='{name}']/ancestor::div[contains(@class,'p-4')][1]")

    def ADD_BTN_IN_CARD(self, name: str):
        # Tombol Add to Cart berada di dalam card root
        return (By.XPATH, f"//h3[normalize-space()='{name}']/ancestor::div[contains(@class,'p-4')][1]"
                          f"//button[.//span[normalize-space()='Add to Cart']]")

    def PRICE_IN_CARD(self, name: str):
        # <span class="text-lg font-bold text-green-600">$99.99</span>
        return (By.XPATH, f"//h3[normalize-space()='{name}']/ancestor::div[contains(@class,'p-4')][1]"
                          f"//span[contains(@class,'text-green-600')]")

    def STOCK_IN_CARD(self, name: str):
        # <span class="text-sm text-gray-500">Stock: 23</span>
        return (By.XPATH, f"//h3[normalize-space()='{name}']/ancestor::div[contains(@class,'p-4')][1]"
                          f"//span[contains(normalize-space(),'Stock:')]")

    # ---- Actions ----
    def search(self, keyword: str):
        box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        box.clear()
        box.send_keys(keyword)
        # kalau app perlu ENTER untuk trigger filter:
        # from selenium.webdriver.common.keys import Keys; box.send_keys(Keys.ENTER)

    # ---- Assertions / getters ----
    def assert_card_visible(self, name: str):
        self.wait.until(EC.visibility_of_element_located(self.NAME_HEADING(name)))

    def get_price_text(self, name: str) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self.PRICE_IN_CARD(name)))
        return el.text.strip()  # e.g. "$99.99"

    def get_stock_number(self, name: str) -> int:
        el = self.wait.until(EC.visibility_of_element_located(self.STOCK_IN_CARD(name)))
        txt = el.text.strip()  # "Stock: 23"
        try:
            return int(txt.split(":")[1].strip())
        except Exception:
            return -1  # fallback

    def add_to_cart_by_name(self, name: str):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_BTN_IN_CARD(name)))
        btn.click()

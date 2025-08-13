# pages/pos_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class PosPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        # Locator
        self.pos_menu = (By.XPATH, "//*[normalize-space()='Point of Sale']")
        self.search_input = (By.CSS_SELECTOR, "input[placeholder^='Search']")
        self.product_card_title = "//h3[normalize-space()='{name}']"
        self.add_to_cart_btn = (
            "//h3[normalize-space()='{name}']/ancestor::div[contains(@class,'p-4')]"
            "//span[normalize-space()='Add to Cart']"
        )

    def go_to_pos_page(self):
        """Klik menu Point of Sale & tunggu search bar muncul."""
        menu_btn = self.wait.until(EC.element_to_be_clickable(self.pos_menu))
        menu_btn.click()
        search_el = self.wait.until(EC.visibility_of_element_located(self.search_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_el)

    def search_product(self, product_name):
        """Cari produk di halaman POS."""
        self.go_to_pos_page()
        search_el = self.wait.until(EC.visibility_of_element_located(self.search_input))
        search_el.clear()
        search_el.send_keys(product_name)
        try:
            search_el.send_keys(Keys.RETURN)  # trigger filter kalau perlu
        except:
            pass
        # Tunggu produk muncul
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.product_card_title.format(name=product_name))
        ))

    def select_product(self, product_name):
        """Klik Add to Cart produk."""
        btn_locator = (By.XPATH, self.add_to_cart_btn.format(name=product_name))
        add_btn = self.wait.until(EC.element_to_be_clickable(btn_locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        add_btn.click()

    def increase_quantity(self, product_name):
        """Klik tombol + untuk produk di cart."""
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//td[contains(., '{product_name}')]/..//button[contains(., '+')]")
        ))
        btn.click()

    def decrease_quantity(self, product_name):
        """Klik tombol - untuk produk di cart."""
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//td[contains(., '{product_name}')]/..//button[contains(., '-')]")
        ))
        btn.click()

    def remove_from_cart(self, product_name):
        """Klik tombol Remove untuk produk di cart."""
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//td[contains(., '{product_name}')]/..//button[contains(., 'Remove')]")
        ))
        btn.click()

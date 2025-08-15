from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Sidebar:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click_menu(self, menu_name):
        """Klik menu berdasarkan text di sidebar"""
        menu_btn = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//span[normalize-space()='{menu_name}']/ancestor::button"
        )))
        menu_btn.click()

    def go_to_transactions(self):
        self.click_menu("Transactions")

    def go_to_reports(self):
        self.click_menu("Reports")

    def go_to_pos(self):
        self.click_menu("Point of Sale")

    def logout(self):
        self.click_menu("Sign Out")

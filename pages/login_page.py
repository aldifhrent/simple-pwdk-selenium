# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, base_url=None, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/") if base_url else None
        self.wait = WebDriverWait(driver, timeout)

        # Locator yang sudah disesuaikan dengan AUT
        self.email_input = (By.CSS_SELECTOR, "input[type='email']") 
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

        # Indikator sesudah login sukses - header POS System
        self.dashboard_indicator = (By.CSS_SELECTOR, "h1.text-2xl.font-bold")

        # Indikator error login - Invalid credentials message
        self.login_error = (By.CSS_SELECTOR, ".bg-red-50.border.border-red-200.text-red-600")

    def open(self):
        """Buka halaman login."""
        if self.base_url:
            self.driver.get(self.base_url)
        else:
            raise ValueError("base_url not set")

    def visit(self, url):
        """Visit the specified URL."""
        self.driver.get(url)

    def login(self, email: str, password: str):
        """Isi form login dan submit."""
        email_el = self.wait.until(EC.visibility_of_element_located(self.email_input))
        email_el.clear()
        email_el.send_keys(email)

        pass_el = self.wait.until(EC.visibility_of_element_located(self.password_input))
        pass_el.clear()
        pass_el.send_keys(password)

        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_btn.click()

    def wait_no_error(self):
        """Wait for no error to appear (for successful login)."""
        try:
            self.wait.until(EC.invisibility_of_element_located(self.login_error))
            return True
        except:
            raise AssertionError("Login gagal - error masih muncul")

    def get_pos_header_text(self):
        """Get the POS header text after successful login."""
        header = self.wait.until(EC.visibility_of_element_located(self.dashboard_indicator))
        return header.text

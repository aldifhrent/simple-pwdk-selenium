# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

        # TODO: sesuaikan locator dengan AUT kamu
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

        # Indikator sesudah login sukses (ganti ke elemen yang unik di dashboard)
        self.dashboard_indicator = (By.CSS_SELECTOR, ".dashboard, [data-test='dashboard']")

        # Indikator error login (toast/alert)
        self.login_error = (By.CSS_SELECTOR, ".toast-error, .alert-danger, [data-test='login-error']")

    def open(self):
        """Buka halaman login."""
        self.driver.get(f"{self.base_url}/login")

    def login(self, email: str, password: str):
        """Isi form login dan submit."""
        email_el = self.wait.until(EC.visibility_of_element_located(self.email_input))
        email_el.clear()
        email_el.send_keys(email)

        pass_el = self.wait.unti_

# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    EMAIL     = (By.CSS_SELECTOR, "input[type='email'][placeholder='Enter your email']")
    PASSWORD  = (By.CSS_SELECTOR, "input[type='password'][placeholder='Enter your password']")
    LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Sign In']")
    ERROR_MSG = (By.XPATH, "//div[contains(@class,'text-red-600') and contains(normalize-space(),'Invalid credentials')]")
    POS_HEADER = (By.XPATH, "//h1[normalize-space()='POS System']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visit(self, url: str):
        self.driver.get(url)

    def login(self, email: str, password: str):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL)).clear()
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD)).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()

    def wait_no_error(self):
        # anggap sukses jika error tidak muncul dalam waktu tunggu
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG))
            raise AssertionError("Login gagal: 'Invalid credentials' muncul.")
        except TimeoutException:
            return True

    def get_pos_header_text(self) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self.POS_HEADER))
        return el.text.strip()

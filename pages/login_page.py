# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, base_url=None, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/") if base_url else None
        self.wait = WebDriverWait(driver, timeout)

        # Locators (sesuaikan dengan AUT)
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

        # Indikator sesudah login sukses - header POS System
        self.dashboard_indicator = (By.CSS_SELECTOR, "h1.text-2xl.font-bold")

        # Indikator error login (utama)
        self.login_error = (By.CSS_SELECTOR, ".bg-red-50.border.border-red-200.text-red-600")

        # Beberapa locator alternatif untuk berjaga-jaga (opsional)
        self._error_locators_fallback = [
            (By.CSS_SELECTOR, ".text-red-600"),
            (By.CSS_SELECTOR, ".alert-danger, .toast-error, .error, .error-message"),
            (By.XPATH, "//*[contains(@class,'text-red')][contains(., 'Invalid')]"),
        ]

    # -------------------------
    # Navigation
    # -------------------------
    def open(self):
        """Buka halaman login menggunakan base_url."""
        if self.base_url:
            self.driver.get(self.base_url)
        else:
            raise ValueError("base_url not set")

    def visit(self, url):
        """Visit URL spesifik (biasa dipakai dari fixture test)."""
        self.driver.get(url)

    # -------------------------
    # Actions
    # -------------------------
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

    # -------------------------
    # Assertions / Getters
    # -------------------------
    def wait_no_error(self):
        """Pastikan tidak ada error (untuk login sukses)."""
        try:
            self.wait.until(EC.invisibility_of_element_located(self.login_error))
            return True
        except Exception:
            raise AssertionError("Login gagal - error masih muncul")

    def get_pos_header_text(self):
        """Ambil teks header setelah login sukses."""
        header = self.wait.until(EC.visibility_of_element_located(self.dashboard_indicator))
        return header.text

    def assert_logged_in(self, expected_header="POS System"):
        """Pastikan login sukses dan header sesuai."""
        self.wait_no_error()
        actual_header = self.get_pos_header_text()
        assert actual_header == expected_header, (
            f"Header mismatch. expected={expected_header!r}, actual={actual_header!r}"
        )

    # -------------------------
    # Error helpers (baru)
    # -------------------------
    def error_element(self, timeout: int = 10):
        """
        Cari elemen error menggunakan locator utama, jika gagal coba fallback list.
        Return WebElement jika ketemu, raise Timeout kalau tidak.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(self.login_error))
        except Exception:
            # Coba beberapa fallback yang umum dipakai UI
            for loc in self._error_locators_fallback:
                try:
                    return self.wait.until(EC.visibility_of_element_located(loc))
                except Exception:
                    continue
            # Kalau tetap tidak ketemu, naikkan lagi exception terakhir
            raise

    def get_error_message(self, timeout: int = 10) -> str:
        """
        Tunggu error login terlihat lalu kembalikan text-nya.
        Dipakai di test negatif: lp.get_error_message()
        """
        el = self.error_element(timeout=timeout)
        return el.text.strip()

    def is_error_visible(self, timeout: int = 5) -> bool:
        """
        Cek cepat apakah error terlihat tanpa melempar exception.
        """
        try:
            el = self.error_element(timeout=timeout)
            return el.is_displayed()
        except Exception:
            return False

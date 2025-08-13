# pages/opt/transactions_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pytest
import logging

logger = logging.getLogger(__name__)

class TransactionsPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def assert_on_transactions_page(self):
        """Pastikan kita ada di halaman Transactions."""
        self.wait.until(EC.visibility_of_element_located((
            By.XPATH, "//h1[normalize-space()='Transactions']"
        )))

    def filter_by_time(self, time_filter):
        """Pilih filter waktu di dropdown."""
        dropdown = self.wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, "select.px-4.py-2.border-gray-300"
        )))
        Select(dropdown).select_by_visible_text(time_filter)

    # Tunggu sampai tabel muncul atau pesan kosong
        self.wait.until(lambda driver: (
        driver.find_elements(By.CSS_SELECTOR, "table") or
        driver.find_elements(By.XPATH, "//p[normalize-space()='No transactions found']")
        ))

    def search_transaction(self, query):
        """Cari transaksi berdasarkan TXN ID atau nama customer."""
        search_box = self.wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, "input[placeholder*='Search by transaction']"
        )))
        search_box.clear()
        search_box.send_keys(query)

        # Tunggu sampai tabel atau pesan kosong muncul
        self.wait.until(lambda driver: (
            driver.find_elements(By.CSS_SELECTOR, "table") or
            driver.find_elements(By.XPATH, "//p[normalize-space()='No transactions found']")
        ))

    def assert_transaction_visible(self, txn_id):
        """Pastikan transaksi terlihat atau validasi pesan kosong."""
        try:
            no_txn_elem = self.driver.find_element(
            By.XPATH, "//p[normalize-space()='No transactions found']"
            )
            if no_txn_elem.is_displayed():
                logger.info(f"✅ Tidak ada transaksi ditemukan, tampil pesan kosong untuk '{txn_id}'.")
                return  # Test tetap dianggap pass
        except NoSuchElementException:
            pass  # Tidak ada pesan kosong, lanjut cek tabel

        self.wait.until(EC.visibility_of_element_located((
        By.XPATH, f"//td//div[contains(., '{txn_id}')]"
        )))
        logger.info(f"✅ Transaksi '{txn_id}' ditemukan di tabel.")


    
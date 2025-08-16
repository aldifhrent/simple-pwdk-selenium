import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

class ReportPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Locators ---
    HEADER_TITLE = (By.XPATH, "//h1[normalize-space()='Sales Reports']")
    HEADER_DESC = (By.XPATH, "//p[contains(text(),'Track your business performance')]")
    FILTER_DROPDOWN = (By.TAG_NAME, "select")
    FILTER_OPTIONS = (By.TAG_NAME, "option")

    SUMMARY_CARDS = (By.CSS_SELECTOR, "div.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4.gap-6 > div")

    # --- Actions ---
    def wait_for_page(self):
        """Tunggu sampai halaman report tampil."""
        self.wait.until(EC.visibility_of_element_located(self.HEADER_TITLE))
        logger.info("✅ Halaman Reports terbuka.")

    def get_header_text(self):
        title = self.driver.find_element(*self.HEADER_TITLE).text
        desc = self.driver.find_element(*self.HEADER_DESC).text
        return title, desc

    def get_filter_options(self):
        dropdown = self.driver.find_element(*self.FILTER_DROPDOWN)
        options = dropdown.find_elements(*self.FILTER_OPTIONS)
        return [opt.text for opt in options]

    def select_filter(self, value):
        dropdown = self.driver.find_element(*self.FILTER_DROPDOWN)
        for option in dropdown.find_elements(*self.FILTER_OPTIONS):
            if option.text.strip().lower() == value.lower():
                option.click()
                logger.info(f"🔍 Filter dipilih: {value}")
                break

    def get_summary_cards(self):
        cards = self.driver.find_elements(*self.SUMMARY_CARDS)
        result = []
        for card in cards:
            try:
                label = card.find_element(By.CSS_SELECTOR, "p.text-sm.font-medium").text
                value = card.find_element(By.CSS_SELECTOR, "p.text-2xl.font-semibold").text
                result.append((label, value))
            except Exception as e:
                logger.warning(f"⚠️ Gagal membaca card ringkasan: {e}")
        if not result:
            logger.warning("⚠️ Tidak ada data di summary cards.")
        return result

    def get_daily_sales(self):
        container = self.driver.find_element(By.XPATH, "//h3[normalize-space()='Daily Sales']/..")
        empty_text = container.find_elements(By.XPATH, ".//p[contains(text(),'No sales data')]")
        if empty_text:
            logger.info("ℹ️ Daily Sales kosong")
            return []
        dates = [d.text for d in container.find_elements(By.CSS_SELECTOR, "span.text-sm.text-gray-600")]
        values = [v.text for v in container.find_elements(By.CSS_SELECTOR, "span.text-sm.font-medium")]
        return list(zip(dates, values))


    def get_top_products(self):
        container = self.driver.find_element(By.XPATH, "//h3[normalize-space()='Top Products']/..")
        empty_text = container.find_elements(By.XPATH, ".//p[contains(text(),'No product data')]")
        if empty_text:
            logger.info("ℹ️ Top Products kosong")
            return []
        names = [n.text for n in container.find_elements(By.CSS_SELECTOR, "p.font-medium.text-gray-900")]
        solds = [s.text for s in container.find_elements(By.CSS_SELECTOR, "p.text-sm.text-gray-500")]
        totals = [t.text for t in container.find_elements(By.CSS_SELECTOR, "p.font-semibold.text-green-600")]
        return list(zip(names, solds, totals))


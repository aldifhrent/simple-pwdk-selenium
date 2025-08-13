import logging
import pytest
import os
from datetime import datetime
from pages.login_page import LoginPage
from pages.pos_page import PosPage

logger = logging.getLogger(__name__)

@pytest.mark.smoke
def test_product_search_and_selection(driver, app_url, creds):
    logger.info("🔹 Mulai test Product Search and Selection")

    # Login
    lp = LoginPage(driver)
    lp.visit(app_url)
    logger.info("Buka URL: %s", app_url)
    lp.login(creds["email"], creds["password"])
    logger.info("Login dengan user: %s", creds["email"])
    lp.assert_logged_in()
    logger.info("Login sukses ✅")

    # Search produk di POS
    product_name = "Wireless Headphones"
    pp = PosPage(driver)
    pp.search_product(product_name)
    pp.assert_product_visible(product_name)

    # 📸 Screenshot hasil pencarian
    folder_path = "screenshots/pos"
    os.makedirs(folder_path, exist_ok=True)  # bikin folder kalau belum ada
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{folder_path}/search_result_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    logger.info("Screenshot disimpan: %s", screenshot_path)

    # Pilih produk
    pp.select_product(product_name)

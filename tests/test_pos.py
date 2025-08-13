import logging
import pytest
import os
from datetime import datetime
from pages.login_page import LoginPage
from pages.pos_page import PosPage

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.products
def test_product_search_with_category_filter(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    pp = PosPage(driver)

    search_name = "Wireless"
    pp.search_product(search_name)

    category_name = "Electronics"
    pp.filter_by_category(category_name)

    # Verifikasi produk ada
    pp.assert_product_visible("Wireless Headphones")

    # Screenshot
    folder_path = "screenshots/pos"
    os.makedirs(folder_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"{folder_path}/search_filter_{timestamp}.png")

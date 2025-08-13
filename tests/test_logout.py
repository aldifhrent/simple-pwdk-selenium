from datetime import datetime
import pytest
from pages.login_page import LoginPage
from util.sidebar import Sidebar
from selenium.webdriver.common.by import By
import os

def take_screenshot(driver, name, folder="screenshots"):
    os.makedirs(folder, exist_ok=True)
    driver.save_screenshot(f"{folder}/{name}.png")

@pytest.mark.smoke
@pytest.mark.logout
def test_logout_with_screenshot(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    take_screenshot(driver, f"before-logout-{ts}", folder="screenshots/logout")

    sidebar = Sidebar(driver)
    sidebar.logout()

    take_screenshot(driver, f"after-logout-{ts}", folder="screenshots/logout")

    welcome_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "welcome back" in welcome_text

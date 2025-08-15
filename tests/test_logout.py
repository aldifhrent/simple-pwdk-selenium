from datetime import datetime
import pytest
from pages.login_page import LoginPage
from util.sidebar import Sidebar
from selenium.webdriver.common.by import By
from util.helper import take_screenshot
import os

@pytest.mark.smoke
@pytest.mark.logout
def test_logout_with_screenshot(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    take_screenshot(driver, "before-logout", folder="screenshots/logout")

    sidebar = Sidebar(driver)
    sidebar.logout()

    take_screenshot(driver, "after-logout", folder="screenshots/logout")

    welcome_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "welcome back" in welcome_text

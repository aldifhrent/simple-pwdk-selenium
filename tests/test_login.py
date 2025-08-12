# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from utils.helpers import take_screenshot

@pytest.mark.smoke
def test_login_valid(driver, app_url, creds):
    lp = LoginPage(driver)        # atau LoginPage(driver, app_url) sesuai implementasi kamu
    lp.visit(app_url)             # atau lp.open()
    lp.login(creds["email"], creds["password"])
    lp.should_be_logged_in()

@pytest.mark.regression
def test_login_invalid_password(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], "salahpassword123")
    try:
        lp.should_see_login_error()
    except Exception as e:
        take_screenshot(driver, "login_invalid_failed")
        raise  # atau: raise AssertionError(f"Tidak muncul error login: {e}")

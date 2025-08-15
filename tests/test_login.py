# tests/test_login.py
import logging
from pages.login_page import LoginPage
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.positive
def test_login_valid(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.wait_no_error()

    actual = lp.get_pos_header_text()
    expected = "POS System"

    # log dulu supaya terlihat meskipun pass
    logger.info("Asserting header... expected=%r, actual=%r", expected, actual)
    assert actual == expected, f"Header mismatch. expected={expected!r}, actual={actual!r}"

@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.negative
def test_login_invalid(driver, app_url, creds):
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], "password_salah")
    
    # Tunggu error muncul
    error_element = lp.wait.until(EC.visibility_of_element_located(lp.login_error))
    assert error_element.is_displayed(), "Error message should be displayed for invalid login"
    
    # Verifikasi text error
    error_text = error_element.text
    expected_error = "Invalid credentials"
    assert error_text == expected_error, f"Error message mismatch. expected={expected_error!r}, actual={error_text!r}"
    
    logger.info("Invalid login test passed - error message: %s", error_text)

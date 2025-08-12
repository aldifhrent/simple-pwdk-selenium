# tests/test_login.py
import logging
from pages.login_page import LoginPage
import pytest

logger = logging.getLogger(__name__)

BASE_URL = "https://simple-pos-pwdk.netlify.app/"
EMAIL = "admin@pos.com"
PASSWORD = "admin"

@pytest.mark.smoke
def test_login_valid(driver):
    lp = LoginPage(driver)
    lp.visit(BASE_URL)
    lp.login(EMAIL, PASSWORD)
    lp.wait_no_error()

    actual = lp.get_pos_header_text()
    expected = "POS System"

    # log dulu supaya terlihat meskipun pass
    logger.info("Asserting header... expected=%r, actual=%r", expected, actual)
    assert actual == expected, f"Header mismatch. expected={expected!r}, actual={actual!r}"

def test_login_invalid(driver):
    lp = LoginPage(driver)
    lp.visit(BASE_URL)
    lp.login(EMAIL, "password_salah")
    # kalau error muncul, test PASS; kalau tidak, FAIL
    try:
        lp.wait_no_error()
        raise AssertionError("Seharusnya login gagal, tapi tidak ada error.")
    except AssertionError as e:
        # ini dari wait_no_error: ‘Invalid credentials’ muncul → sesuai harapan
        if "Login gagal" in str(e):
            pass
        else:
            raise

import logging
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

# =======================
# Test Data
# =======================
checkout_cases = [
    ("John Doe", "john@example.com", True, "valid"),   # ✅ Nama + Email → sukses
    ("", "", False, "empty"),                          # ❌ Kosong semua
    ("John Doe", "", False, "name_only"),              # ❌ Hanya nama
    ("", "john@example.com", False, "email_only"),     # ❌ Hanya email
]

payment_methods = ["Cash", "Card", "Digital"]

# =======================
# TEST
# =======================
@pytest.mark.checkout
@pytest.mark.parametrize("name,email,expected,case_id", checkout_cases, ids=[c[3] for c in checkout_cases])
@pytest.mark.parametrize("payment", payment_methods, ids=payment_methods)
def test_checkout(driver, app_url, creds, name, email, expected, case_id, payment):
    """Checkout dengan kombinasi input (nama/email) dan metode pembayaran."""

    # ==== Login ====
    lp = LoginPage(driver)
    lp.visit(app_url)
    lp.login(creds["email"], creds["password"])
    lp.assert_logged_in()

    # ==== Tambah produk ====
    pp = ProductsPage(driver)
    pp.search_product("Wireless Headphones")
    pp.add_to_cart("Wireless Headphones")

    cp = CartPage(driver)

    # ==== Checkout ====
    cp.checkout()
    cp.fill_customer_info(name, email)
    cp.select_payment_method(payment)
    cp.complete_transaction()

    # ==== Ambil alert ====
    alert_text, txid = cp.get_transaction_alert_and_id()

    if expected:
        assert alert_text is not None, f"Expected sukses tapi gagal (case={case_id}, method={payment})"
        assert txid is not None, f"Expected TXID tidak ada (case={case_id}, method={payment}, alert={alert_text})"
        logger.info(f"✅ Sukses checkout {case_id} via {payment}, TXID={txid}")
    else:
        if alert_text and txid:
            pytest.fail(f"BUG: Checkout berhasil padahal harus gagal (case={case_id}, method={payment}, alert={alert_text})")
        logger.info(f"✅ Validasi gagal sesuai harapan ({case_id}, method={payment})")

    take_screenshot(driver, f"checkout_{case_id}_{payment}", folder="screenshots/checkout")

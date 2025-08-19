import logging
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from util.helper import take_screenshot

logger = logging.getLogger(__name__)

# =======================
# Test Data
# =======================
checkout_cases = [
    ("John Doe", "john@example.com", True, "valid"),
    ("", "", False, "empty"),
    ("John Doe", "", False, "name_only"),
    ("", "john@example.com", False, "email_only"),
]

payment_methods = ["Cash", "Card", "Digital"]


# =======================
# TEST
# =======================
@pytest.mark.checkout
@pytest.mark.parametrize(
    "name,email,expected,case_id", checkout_cases, ids=[c[3] for c in checkout_cases]
)
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
    cp.checkout()
    cp.fill_customer_info(name, email)
    cp.select_payment_method(payment)

    # ==== Positive Case (expected=True) ====
    if expected:
        cp.complete_transaction()

        # Ambil alert dan TXID
        alert_text, txid = cp.get_transaction_alert_and_id()
        assert (
            alert_text is not None
        ), f"Expected sukses tapi gagal (case={case_id}, method={payment})"
        assert (
            txid is not None
        ), f"TXID tidak ada (case={case_id}, method={payment}, alert={alert_text})"

        # 🔗 Integrasi ke Transactions page
        assert cp.check_transactions_on_transaction_page(
            txid
        ), f"Transaksi {txid} tidak tercatat di halaman Transactions"

        logger.info(f"✅ Sukses checkout {case_id} via {payment}, TXID={txid}")

    # ==== Negative Case (expected=False) ====
    else:
        try:
            btn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(., 'Complete Transaction')]")
                )
            )
            if btn.is_enabled():
                btn.click()
                alert_text, txid = cp.get_transaction_alert_and_id()
                # logger.error(
                #     f"⚠️ BUG: Checkout berhasil padahal harusnya gagal "
                #     f"(case={case_id}, method={payment}, alert={alert_text}, TXID={txid})"
                # )
                pytest.fail(
                f"BUG: Checkout berhasil padahal harusnya gagal "
                f"(case={case_id}, method={payment}, alert={alert_text}, TXID={txid})"
            )
            else:
                logger.info(
                    f"✅ Tombol Complete Transaction disabled sesuai harapan ({case_id}, {payment})"
                )
        except Exception:
            logger.info(
                f"✅ Tidak ada tombol Complete Transaction (validasi gagal sesuai harapan) ({case_id}, {payment})"
            )

    # ==== Screenshot untuk evidence ====
    take_screenshot(
        driver, f"checkout_{case_id}_{payment}", folder="screenshots/checkout"
    )

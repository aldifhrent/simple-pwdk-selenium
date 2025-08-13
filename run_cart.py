# run_pos_smoke.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "https://simple-pos-pwdk.netlify.app/"
EMAIL = "admin@pos.com"
PASSWORD = "admin"

HEADLESS = False     # <-- set True kalau mau headless
KEEP_OPEN = True     # <-- biar bisa lihat hasilnya sebelum close

def main():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")

    print("[INIT] Open Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    wait = WebDriverWait(driver, 10)

    try:
        # --- Login ---
        print("[STEP 1] Open login page")
        driver.get(BASE_URL)

        print("[STEP 2] Fill credentials")
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='email'][placeholder='Enter your email']"))
        ).send_keys(EMAIL)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='password'][placeholder='Enter your password']"))
        ).send_keys(PASSWORD)

        print("[STEP 3] Click Sign In")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Sign In']"))
        ).click()

        print("[STEP 4] Assert header 'POS System'")
        h1 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h1[normalize-space()='POS System']"))
        )
        assert h1.text.strip() == "POS System", "Header POS System tidak muncul!"
        print("✅ Login OK")

        # --- Search & Add to Cart ---
        product = "Wireless Headphones"
        print(f"[STEP 5] Search: {product}")
        box = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search products...']"))
        )
        box.clear(); box.send_keys(product)

        print("[STEP 6] Assert product card visible")
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//h3[normalize-space()='{product}']"))
        )

        print("[STEP 7] Click 'Add to Cart' on that product")
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//h3[normalize-space()='{product}']/ancestor::div[contains(@class,'p-4')][1]"
                       f"//button[.//span[normalize-space()='Add to Cart']]"))
        )
        add_btn.click()

        print("✅ Add to Cart OK")

        # OPTIONAL: tunggu user cek hasil
        if KEEP_OPEN and not HEADLESS:
            input("[INFO] Tekan Enter untuk menutup browser...")

    except (AssertionError, TimeoutException) as e:
        print(f"❌ Gagal: {e}\n📸")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

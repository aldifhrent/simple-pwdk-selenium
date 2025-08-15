from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

def base_url():
    return "https://simple-pos-pwdk.netlify.app/"

def credentials():
    return {"email": "admin@pos.com", "password": "admin"}

def is_headless():
    return False    # set False kalau mau lihat browsernya

def take_screenshot(driver, name, folder="screenshots"):
    # Buat folder kalau belum ada
    path = os.path.join(folder)
    os.makedirs(path, exist_ok=True)
    
    # Tambahkan timestamp biar unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(path, f"{name}_{timestamp}.png")

    driver.save_screenshot(file_path)
    return file_path

def click_button_by_text(driver, text, timeout=10):
    wait = WebDriverWait(driver, timeout)
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[contains(normalize-space(), '{text}')]")
        )
    )
    btn.click()
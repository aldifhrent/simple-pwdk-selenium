from datetime import datetime

def base_url():
    return "https://simple-pos-pwdk.netlify.app/"

def credentials():
    return {"email": "admin@pos.com", "password": "admin"}

def is_headless():
    return False    # set False kalau mau lihat browsernya

def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def take_screenshot(driver, name_prefix="screenshot"):
    filename = f"{name_prefix}_{_ts()}.png"
    driver.save_screenshot(filename)
    print(f"[screenshot] {filename}")

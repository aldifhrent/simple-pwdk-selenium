from datetime import datetime

def base_url():
    return "https://simple-pos-pwdk.netlify.app/"

def credentials():
    # Credentials login to access simple pos
    return {
        "email": "admin@pos.com",
        "password": "admin"
    }

def is_headless():
    # True = headless mode, False = lihat browsernya
    return True

def timestamp():
    # Timestamp untuk nama file screenshot atau laporan
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def take_screenshot(driver, name_prefix="screenshot"):
    # Simpan screenshot dengan timestamp
    filename = f"{name_prefix}_{timestamp()}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")

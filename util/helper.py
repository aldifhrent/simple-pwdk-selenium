from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def base_url():
    return "https://simple-pos-pwdk.netlify.app/"

def credentials():
    return {"email": "admin@pos.com", "password": "admin"}

def is_headless():
    return False    # set False kalau mau lihat browsernya

def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

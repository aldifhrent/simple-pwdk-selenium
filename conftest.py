import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from data.config import BASE_URL, ADMIN


@pytest.fixture(scope="session")
def app_url():
    """URL utama aplikasi."""
    return BASE_URL


@pytest.fixture(scope="session")
def creds():
    """Kredensial admin."""
    return ADMIN


@pytest.fixture(scope="function")
def driver():
    """Fixture WebDriver yang cepat & aman untuk macOS."""
    opts = Options()

    # Jalankan headless jika tidak perlu lihat browser
    opts.add_argument("--headless=new")  # Comment kalau mau lihat browser
    opts.add_argument("--window-size=1440,1080")

    # Optimisasi startup
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # Hapus --start-maximized biar startup lebih cepat di headless
    
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

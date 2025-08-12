import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from data.config import BASE_URL, ADMIN

@pytest.fixture(scope="session")
def app_url(): return BASE_URL

@pytest.fixture(scope="session")
def creds(): return ADMIN  # {"email": "...", "password": "..."}

@pytest.fixture(scope="function")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")   # tampilkan UI? comment baris ini
    opts.add_argument("--window-size=1920,1080")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import base_url, credentials, is_headless

@pytest.fixture(scope="session")
def app_url():
    return base_url()

@pytest.fixture(scope="session")
def creds():
    return credentials()

@pytest.fixture(scope="function")
def driver():
    opts = Options()
    if is_headless():
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

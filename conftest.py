import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from data.config import BASE_URL, ADMIN

@pytest.fixture(scope="session")
def app_url(): return BASE_URL

@pytest.fixture(scope="session")
def creds(): return ADMIN 

@pytest.fixture(scope="function")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")   # COMMENT OUT UNTUK MELIHAT BROWSER
    opts.add_argument("--window-size=1440,1080")
    opts.add_argument("--start-maximized")  # Browser akan full screen
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

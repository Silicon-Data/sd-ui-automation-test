import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller


@pytest.fixture(scope="session")
def driver():
    chromedriver_path = chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")  # 设置为常见的 1080p 分辨率
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(executable_path=chromedriver_path),
        options=chrome_options
    )
    yield driver
    driver.quit()
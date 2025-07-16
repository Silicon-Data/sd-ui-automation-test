import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from datetime import datetime


@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
    chrome_options.add_argument("--disable-extensions")  # 禁用扩展
    chrome_options.add_argument("--disable-infobars")  # 禁用"Chrome正在被自动化控制"提示
    chrome_options.add_argument("--disable-notifications")  # 禁用通知
    chrome_options.add_argument("--disable-plugins-discovery")  # 禁用插件发现
    chrome_options.add_argument("--log-level=3")  # 仅显示致命错误

    # 禁用不必要的网络活动
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    driver = webdriver.Chrome(
        service=Service(executable_path='/usr/local/bin/chromedriver'),
        options=chrome_options
    )
    yield driver
    driver.quit()

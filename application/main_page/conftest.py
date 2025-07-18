import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller  # 自动安装 chromedriver

@pytest.fixture(scope="module")
def driver():
    # 自动安装 chromedriver
    chromedriver_path = chromedriver_autoinstaller.install()

    # 无头模式配置
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 新版本的 headless 模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 配置 Chrome Driver
    driver = webdriver.Chrome(
        service=Service(executable_path=chromedriver_path),  # 设置 chromedriver 路径
        options=chrome_options  # 设置浏览器选项
    )

    # 提供 driver 供测试用例使用
    yield driver

    # 测试结束后关闭浏览器
    driver.quit()
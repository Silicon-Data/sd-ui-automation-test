import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


@pytest.fixture(scope="module")
def driver():
    # 自动安装/匹配 chromedriver（推荐显式指定路径）
    chromedriver_path = chromedriver_autoinstaller.install()  # 返回驱动路径

    # 无头模式配置（增强稳定性）
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 无头模式
    chrome_options.add_argument("--no-sandbox")  # 禁用沙盒（必须）
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
    chrome_options.add_argument("--window-size=1920,1080")  # 设置默认窗口大小

    # 初始化浏览器（显式指定驱动路径）
    driver = webdriver.Chrome(
        executable_path=chromedriver_path,  # 使用自动安装的路径
        options=chrome_options
    )

    yield driver
    driver.quit()
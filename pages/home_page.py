from time import sleep
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from application.conftest import driver
from pages.base_page import BasePage
from pages.login.login_page import LoginPage


class HomePage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'text-white') and contains(text(), 'Log In')]")
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login(self) -> LoginPage:
        login_page_url = "https://www.silicondata.com/signin"
        try:
            self.driver.find_element(*self.LOGIN_BUTTON)
            self.driver.execute_script("""
                    var cookieBanner = document.getElementById('CybotCookiebotDialog');
                    if (cookieBanner) cookieBanner.remove();
                """)
            sleep(1)
            self.click_element(self.LOGIN_BUTTON)
            self.wait_for_page(login_page_url)
            return LoginPage(self.driver)
        except Exception as e:
            pytest.fail(f"loading login page failed: {str(e)}")

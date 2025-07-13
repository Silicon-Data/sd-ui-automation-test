import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "/html/body/section/main/div/div/form/div[1]/input")
    PASSWORD_INPUT = (By.XPATH, '//*[@id="password"]')
    CHECKBOX = (By.XPATH, '//*[@id="checkbox"]')
    SUBMIT_BUTTON = (By.XPATH, '/html/body/section/main/div/div/form/button')
    navigator_page_url = "https://www.silicondata.com/silicon-navigator"
    def __init__(self, driver):
        super().__init__(driver)

    def enter_credentials_and_direct_navigator(self, email, password):
        try:
            self.enter_text(self.EMAIL_INPUT, email)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.click_element(self.CHECKBOX)
            self.click_element(self.SUBMIT_BUTTON)
            self.wait_for_page(self.navigator_page_url)
            if self.driver.current_url == self.navigator_page_url:
                return True, ""
            else:
                error_msg = f"current url {self.driver.current_url} is different from url {self.navigator_page_url}]."
                return False, error_msg

        except Exception as e:
            return False, str(e)

    def submit_login_form(self):
        self.click_element(self.SUBMIT_BUTTON)
        # 返回登录成功后可能跳转的页面，如DashboardPage
        # return DashboardPage(self.driver)
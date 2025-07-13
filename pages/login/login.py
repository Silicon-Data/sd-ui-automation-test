from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")  # 需根据实际页面调整选择器
    PASSWORD_INPUT = (By.ID, "password")  # 需根据实际页面调整选择器
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Submit')]")  # 需根据实际页面调整

    def __init__(self, driver):
        super().__init__(driver)

    def enter_credentials(self, email, password):
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        return self

    def submit_login_form(self):
        self.click_element(self.SUBMIT_BUTTON)
        # 返回登录成功后可能跳转的页面，如DashboardPage
        # return DashboardPage(self.driver)
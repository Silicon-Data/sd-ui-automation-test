from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_page(self, page_url):
        return WebDriverWait(self.driver, 10).until(
            EC.url_to_be(page_url)
        )

    def click_element(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    def enter_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
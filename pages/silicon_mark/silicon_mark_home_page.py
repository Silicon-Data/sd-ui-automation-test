import time
from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from pages.base_page import BasePage
from util.util import dump_all_elements


class SiliconMarkHomePage(BasePage):
    MARK_TAB = (By.XPATH, "(//a)[10]")
    BENCHMARK_PLAN_SEARCH_BOX = (
        By.XPATH, '//button[@data-sentry-element="SelectTrigger" and .//span[contains(., "Please select the benchmark test")]]')
    JOB_NAME_SEARCH_BOX = (By.XPATH, "//input[@placeholder='Please search job name']")
    CREATE_JOB_BUTTON = (By.XPATH, "//button[normalize-space()='Create Job']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_silicon_mark(self):
        silicon_mark_page_url = "https://www.silicondata.com/silicon-mark"
        print(f"self.driver.current_url={self.driver.current_url}")

        try:
            print(self.driver.current_url)
            self.driver.find_element(*self.MARK_TAB)
            self.click_element(self.MARK_TAB)
            self.wait_for_page(silicon_mark_page_url)
            current_url = self.driver.current_url
            if current_url != silicon_mark_page_url:
                pytest.fail(f"Jumped to a wrong url, target url is {silicon_mark_page_url}, but it's {current_url}")

        except AssertionError as e:
            pytest.fail(f"Failed to navigate to silicon mark,error {str(e)}")
        except (TimeoutException, WebDriverException) as e:
            pytest.fail(f"Time out or webdriver error, {str(e)}")
        except Exception as e:
            pytest.fail(f"Failed to navigate to silicon-mark unknown error: {str(e)}")

    def silicon_mark_elements_exist(self):
        print(f"===========>{self.driver.current_url}================")
        time.sleep(3)
        try:
            self.driver.find_element(*self.BENCHMARK_PLAN_SEARCH_BOX)
            self.driver.find_element(*self.JOB_NAME_SEARCH_BOX)
            self.driver.find_element(*self.CREATE_JOB_BUTTON)
        except Exception as e:
            pytest.fail(f"Failed to locate silicon mark elements, error {str(e)}")
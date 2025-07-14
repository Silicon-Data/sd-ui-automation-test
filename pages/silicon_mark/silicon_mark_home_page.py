import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from pages.base_page import BasePage


class SiliconMarkHomePage(BasePage):
    MARK_TAB = (By.XPATH, '//a[@href="/silicon-mark" and .//div[contains(., "SiliconMark")]]')
    BENCHMARK_PLAN_SEARCH_BOX = (By.XPATH, '/html/body/div[2]/div[3]/main/div/div[2]/div/button')
    JOB_NAME_SEARCH_BOX = (By.XPATH, '/html/body/div[2]/div[3]/main/div/div[2]/div/div/input')
    CREATE_JOB_BUTTON = (By.XPATH, '/html/body/div[2]/div[3]/main/div/div[4]/button')

    # DROPDOWN_TRIGGER_LOCATOR = (
    #     By.XPATH,
    #     '//button[contains(@class, "flex h-10 items-center justify-between rounded-md") and .//span[text()="Please select the benchmark test"]]'
    # )

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
        try:
            self.driver.find_element(*self.BENCHMARK_PLAN_SEARCH_BOX)
            self.driver.find_element(*self.JOB_NAME_SEARCH_BOX)
            self.driver.find_element(*self.CREATE_JOB_BUTTON)
        except Exception as e:
            pytest.fail(f"Failed to locate silicon mark elements, error {str(e)}")
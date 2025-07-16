from time import sleep
import pytest
from pages.home_page import HomePage
from pages.silicon_mark.silicon_mark_create_job_page import SiliconMarkCreateJobPage
from pages.silicon_mark.silicon_mark_home_page import SiliconMarkHomePage
from application.conftest import driver

silicon_mark_page = SiliconMarkHomePage(driver)


@pytest.mark.order(1)
def test_successful_login(driver):
    driver.get("https://www.silicondata.com")
    home_page = HomePage(driver)
    print(f"current_page is {driver.current_url}")
    login_page_object = home_page.navigate_to_login()
    is_login, login_message = login_page_object.enter_credentials_and_direct_navigator("frank+protest_internal@silicondata.com", "qqq111!!")
    assert is_login, login_message

@pytest.mark.order(2)
def test_silicon_mark_page_elements_exist(driver):
    window_size = driver.get_window_size()
    print(window_size)
    # return
    print(f"test_silicon_mark_page_elements_exist=>{driver.current_url}")
    silicon_mark_page = SiliconMarkHomePage(driver)
    sleep(2)
    print(f"==----------------=>{driver.current_url}")
    silicon_mark_page.navigate_to_silicon_mark()
    silicon_mark_page.silicon_mark_elements_exist()

def test_create_job(driver):
    print(f"test_create_job==> current_page is {driver.current_url}")

    create_job_page_object = SiliconMarkCreateJobPage(driver)
    create_job_page_object.create_job()
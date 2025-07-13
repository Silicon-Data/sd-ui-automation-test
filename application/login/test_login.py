import pytest
from selenium.webdriver.common.by import By
from application.conftest import driver
from pages.home_page import HomePage


@pytest.mark.run(order=1)
def test_successful_login(driver):
    driver.get("https://www.silicondata.com")

    home_page = HomePage(driver)

    login_page_object = home_page.navigate_to_login()
    is_login, login_message = login_page_object.enter_credentials_and_direct_navigator("frank+protest_internal@silicondata.com", "qqq111!!")
    assert is_login, login_message
    # 使用测试账号登录
    # login_page.enter_credentials("test@example.com", "password123")
    # login_page.submit_login_form()
    #
    # 断言登录成功后的验证逻辑
    # assert driver.current_url == "https://www.silicondata.com/silicon-navigator"
    # assert driver.find_element(By.CSS_SELECTOR, ".user-profile").is_displayed()
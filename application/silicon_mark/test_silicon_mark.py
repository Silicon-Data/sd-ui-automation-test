import pytest
from pages.silicon_mark.silicon_mark_home_page import SiliconMarkHomePage


@pytest.mark.order(3)
def test_navigate_to_silicon_mark(driver):
    print(f"========== siliconmark ==> {driver.current_url}")
    # silicon_mark_home_page = SiliconMarkHomePage(driver)
    # silicon_mark_home_page.navigate_to_silicon_mark()

# @pytest.mark.order(4)
# def test_all_mark_elements_exist(driver):
#     """
#     Confirm all necessary elements are present.
#     :param driver:
#     :return:
#     """
#     silicon_mark_home_page = SiliconMarkHomePage(driver)
#     silicon_mark_home_page.navigate_to_silicon_mark()
#     # silicon_mark_home_page




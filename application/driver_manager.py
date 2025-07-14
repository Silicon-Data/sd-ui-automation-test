# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# import chromedriver_autoinstaller
#
#
# class DriverManager:
#     _instance = None
#
#     @staticmethod
#     def get_instance():
#         if DriverManager._instance is None:
#             DriverManager._instance = DriverManager()
#         return DriverManager._instance
#
#     def __init__(self):
#         self.driver = None
#
#     def init_driver(self):
#         if self.driver is None:
#             chromedriver_path = chromedriver_autoinstaller.install()
#             chrome_options = Options()
#             chrome_options.add_argument("--headless=new")
#             chrome_options.add_argument("--no-sandbox")
#             chrome_options.add_argument("--disable-dev-shm-usage")
#             self.driver = webdriver.Chrome(
#                 service=Service(executable_path=chromedriver_path),
#                 options=chrome_options
#             )
#         return self.driver
#
#     def quit(self):
#         if self.driver:
#             self.driver.quit()
#             self.driver = None
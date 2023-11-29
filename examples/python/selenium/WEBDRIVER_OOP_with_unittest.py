import unittest
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls, new: bool = False) -> None:
        if new:
            options: FirefoxOptions = FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

            cls.driver: Firefox = Firefox(options=options)
            cls.driver.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    @classmethod
    def firefox_scroll(cls, e: WebElement):
        x = e.location["x"]
        y = e.location["y"]
        scroll_by_coord = f"window.scrollTo({x}, {y});"
        scroll_nav_out_of_way = "window.scrollBy(0, -120);"
        cls.driver.execute_script(scroll_by_coord)
        cls.driver.execute_script(scroll_nav_out_of_way)

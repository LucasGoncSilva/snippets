from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement


options: FirefoxOptions = FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver: Firefox = Firefox(options=options)
driver.implicitly_wait(30)

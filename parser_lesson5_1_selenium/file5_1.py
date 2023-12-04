import time
from selenium import webdriver

with webdriver.Chrome() as driver:
    driver.get("https://stepik.org/a/104774")
    time.sleep(5)

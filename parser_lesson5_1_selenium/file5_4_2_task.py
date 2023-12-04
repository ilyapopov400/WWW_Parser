import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

with webdriver.Chrome() as driver:
    driver.get('https://parsinger.ru/selenium/2/2.html')
    link = driver.find_element(By.LINK_TEXT, "16243162441624")
    link.click()

    result = driver.find_element(By.ID, "result").text
    ic(result)

    time.sleep(2)


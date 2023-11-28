from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

url = 'http://parsinger.ru/selenium/3/3.html'
with webdriver.Chrome() as browser:
    browser.get(url)
    link = browser.find_element(By.CLASS_NAME, 'text')
    ic(type(link), link.text.split())

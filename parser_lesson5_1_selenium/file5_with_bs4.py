from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://parsinger.ru/selenium/3/3.html'

# Использование контекстного менеджера для управления WebDriver
with webdriver.Chrome() as browser:
    browser.get(url)
    html_content = browser.page_source

# Парсинг HTML с BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Поиск всех элементов div с классом 'text'
divs = soup.find_all('div', class_='text')

# Вывод результатов
for div in divs:
    print(div.text)

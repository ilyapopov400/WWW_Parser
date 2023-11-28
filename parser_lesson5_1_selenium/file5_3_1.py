from selenium import webdriver
from selenium.webdriver.common.by import By

proxy_list = ['138.199.48.1:8443',
              '209.126.124.140:3128',
              '35.236.207.242:33333',
              '34.82.224.175:33333',
              '163.172.31.44:80', ]

for PROXY in proxy_list:
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        url = 'https://2ip.ru/'

        with webdriver.Chrome(options=chrome_options) as browser:
            browser.get(url)
            print(browser.find_element(By.ID, 'd_clip_button').find_element(By.TAG_NAME, 'span').text)

            browser.set_page_load_timeout(10)

            proxy_list.remove(PROXY)
    except Exception as _ex:
        print(f"Превышен timeout ожидания для - {PROXY}")
        continue

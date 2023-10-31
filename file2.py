#  выводит список должностей и ФИО сотрудника

import requests
import bs4

from creater_dir_file import create_dir, f_ua, record_file

DIR_NAME = 'admin'

URL = "http://policlinic2v.ru/about/administraciya/"

response = requests.get(url=URL, stream=True, headers=f_ua())

if response.status_code:
    print('Status code: {}'.format(response.status_code))
    html_doc = response.text
else:
    print('Status code: {}'.format(response.status_code))

soup = bs4.BeautifulSoup(html_doc, 'html.parser')

content_search = soup.find(name='section', attrs={'id': 'content'})
content_search = content_search.find(name='div', attrs={'id': 'post-1240'})
content_search = content_search.find(name='div', attrs={'class': 'entry clearfix'})
table_admin = content_search.find_all(name='tr')

for i in table_admin:
    special, name = i.find_all(name='td')[0].text, i.find_all(name='td')[1].text
    if bool(special) and bool(name):
        print(special.strip().replace('\n', ''), ':', name.strip().replace('\n', ''))
        print('*' * 33)

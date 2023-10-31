#  сбор фото администрации с сайта поликлиники
import requests
import bs4
import lxml
import html5lib

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

img_list = soup.find('section', {'id': 'content'}).find_all(name='img', alt=True)
href_list = list()

for i in img_list:
    href_list.append(i)

create_dir(name_dir=DIR_NAME)  # создаем, если ее нет директорию

for index, i in enumerate(href_list):
    file_name = i.get('alt').split()[0]
    url = i.get('src')
    record_file(url=url, name_dir=DIR_NAME, name_file=file_name)

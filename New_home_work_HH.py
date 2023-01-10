import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

headers = Headers(browser='firefox', os='win').generate()
hh_html_main = requests.get(HOST, headers=headers).text

TO_NEED_ = ["Django", "Flask"] 
dolars = 'USD'
cursor = 0
all_vacancys = {}
soup = BeautifulSoup(hh_html_main, features = 'lxml')
articles_all = soup.find(class_='vacancy-serp-content')
article_tags = articles_all.find_all(class_="vacancy-serp-item__layout")

for article in article_tags:
    vacancy_name = article.find('a', class_ = 'serp-item__title')
    link = vacancy_name['href']
    fool_vacancy = requests.get(link, headers=headers).text
    soup_vacancy = BeautifulSoup(fool_vacancy, features = 'lxml')
    detail_vacancy = soup_vacancy.find(class_ = 'g-user-content')
    salary_vacancy = soup_vacancy.find(class_ = 'bloko-header-section-2 bloko-header-section-2_lite')
    detail_vacancy_text = detail_vacancy.text
        
    for item in TO_NEED_:
        if item in detail_vacancy_text:
            name_company = article.find('a', class_ = 'bloko-link bloko-link_kind-tertiary') 
            city = article.find('div', class_ = "bloko-text", attrs = {'data-qa': 'vacancy-serp__vacancy-address'})
            data_vacancy = {}
            data_vacancy['Ссылка на вакансию'] = link
            data_vacancy['Вилка зп'] = salary_vacancy.text
            data_vacancy['Название компании'] = name_company.text
            data_vacancy['Город'] = city.text
            cursor += 1
            count = (f' Подходящие вакансия {cursor}')
            all_vacancys[count] = data_vacancy
                        
pprint(all_vacancys)                  
    
with open ('needing_vacancy.json', 'w', encoding = 'utf-8') as nv:
    json.dump(all_vacancys, nv, ensure_ascii=False, indent=4)
    
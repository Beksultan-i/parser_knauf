from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import urlopen
URL = 'https://www.remont3000.ru/catalog/shtukaturnye_smesi/'
HOST = 'https://www.remont3000.ru'
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
FILE = 'remont.csv'
def get_html(URL, params=None):
    r = requests.get(URL, headers=HEADERS, params=params)
    return r

def get_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-item-container')
    knauf_urls = []
    contents = []

    for item in items:
        url = HOST + item.find('a', class_='link_block pos_abs').get('href')
        knauf_urls.append(url)
    
    for knauf_url in knauf_urls:
        req = requests.get(knauf_url, headers=HEADERS)
        soup = BeautifulSoup(urlopen(knauf_url), 'html.parser')
        picture = soup.find('img', class_="pos_abs").get('src'),
        title = soup.find('h1', class_='h1').get_text(strip=True)
        character = soup.find('div', class_='chars after_clr').get_text(strip=True)
        descriptions = soup.find('div', class_='text_desc border_box').find('p').get_text(strip=True)
        
    
        contents.append(
            {
                'picture': picture,
                'title': title,
                'character': character,
                'descriptions': descriptions,
                
            }
        )

            
    with open(FILE, 'w', newline='', encoding='utf-8') as file: 
        writer = csv.writer(file, delimiter=';')
        # writer.writerow(['Фото', 'Название', 'Характеристика', 'Описание'])
        for content in contents:
            writer.writerow(
                [
                    content['picture'], 
                    content['title'],
                    content['character'],
                    content['descriptions']
                ]
            )

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_link(html.text)
    else: 
        print('error')

parse() 
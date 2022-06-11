import re
import requests
from bs4 import BeautifulSoup
from convert_json import save_json

URL = 'https://monomax.by/map'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
HOST = 'https://monomax.by'
FILE = 'monomax.json'


def get_html(url):
    """Send a GET()-request to the site and return the result"""
    result = requests.get(url, headers=HEADERS)
    if result.status_code == 200:
        return result
    raise Exception(f'Connection error {result.status_code}')


def get_content(html):
    """Create a list of dictionaries with data and return it"""
    num = 0
    soup = BeautifulSoup(html.text, 'lxml')
    items = soup.find_all('div', class_='shop')
    raw_geo_from_js = str(soup.find_all('script')[-1])
    coordinates = re.findall(r'\d+\.\d+,\s+\d+\.\d+', raw_geo_from_js)[1:]

    shops = []
    for item in items:

        address = item.find('p', class_='name').get_text()
        phone = item.find('p', class_='phone').get_text()
        coord = coordinates[num]
        shops.append(
            {
                'address': address,
                'latlon': coord,
                'name': 'Monomax',
                'phones': phone,

            }
        )
        num += 1
    return shops


def parse():
    """The main function of the parsing site"""
    html = get_html(URL)
    shops = get_content(html)
    save_json(shops, FILE)


if __name__ == '__main__':
    parse()

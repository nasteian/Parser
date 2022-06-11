from urllib.request import urlopen
import json
from convert_json import save_json

URL = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'
FILE = 'ziko.json'


def get_data(url):
    """Open url and loading to json"""
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json


def get_content(data_json):
    """Create a list of dictionaries with data and return it"""
    shops = []

    converted_list = list(data_json)
    for i in range(len(converted_list)):
        key = converted_list[i]
        value = data_json.get(key)

        shops.append(
            {
                'adress': value.get('city_name')[0] + ' ' + value.get('address'),
                'latlon': value.get('lat') + ',' + value.get('lng'),
                'name': value.get('title'),
                'working_hours': value.get('mp_pharmacy_hours').replace('<br>', ' '),
            }
        )
    return shops


def parse():
    """The main function of the parsing site"""
    html = get_data(URL)
    shops = get_content(html)
    save_json(shops, FILE)


if __name__ == '__main__':
    parse()





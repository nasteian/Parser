from urllib.request import urlopen
import json
from convert_json import save_json

URL = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
FILE = 'kfc.json'


def get_data(url):
    """Open url and loading to json"""
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json


def get_content(data_json):
    """Create a list of dictionaries with data and return it"""
    restaurants = []

    for item in data_json['searchResults']:

        address = item['storePublic']['contacts']['streetAddress'].get('ru', False)
        latlon = item['storePublic']['contacts']['coordinates']['geometry'].get('coordinates', False)
        name = item['storePublic']['title'].get('ru', False)
        phone = item['storePublic']['contacts'].get('phoneNumber', False)

        check_work_time = item['storePublic']['openingHours']['regular'].get('startTimeLocal', False)
        if check_work_time is None:
            working_hours = ['closed']
        else:
            weekdays_from = item['storePublic']['openingHours']['regularDaily'][0]['timeFrom'][0:5]
            weekdays_to = item['storePublic']['openingHours']['regularDaily'][0]['timeTill'][0:5]
            weekends_from = item['storePublic']['openingHours']['regularDaily'][5]['timeFrom'][0:5]
            weekends_to = item['storePublic']['openingHours']['regularDaily'][5]['timeTill'][0:5]
            working_hours = [f'пн - пт {weekdays_from} до {weekdays_to}', f'сб-вс {weekends_from}-{weekends_to}']

        restaurants.append(
            {
                'address': address,
                'latlon': latlon,
                'name': name,
                'phones': phone,
                'working_hours': working_hours
            }
        )
    return restaurants


def parse():
    """The main function of the parsing site"""
    html = get_data(URL)
    shops = get_content(html)
    save_json(shops, FILE)


if __name__ == '__main__':
    parse()

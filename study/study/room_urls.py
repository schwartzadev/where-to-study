import requests
from bs4 import BeautifulSoup
import re
import json
import os
from pathlib import Path

CACHED_FILE_PATH = Path('rooms_urls.json')

def cache() -> dict:
    """
    Cache the room urls data

    @return: the rooms urls data
    """
    response = requests.get('https://www.colorado.edu/students/find-your-study-spot')
    soup = BeautifulSoup(response.content, features="html.parser")

    all_cards = soup.find_all('div', {'class': 'content-grid-item-inner'})

    building_cards = [
        card for card in all_cards if card.find('h2', {'class': 'feature-callout-title'}) is not None
    ]

    data = {}

    for building in building_cards:
        content = {}
        content['title'] = building.find('h2', {'class': 'feature-callout-title'}).text

        room_elements = building.find_all('li')
        rooms = [{'destination': room.find('a')['href'].split('?ce/')[0], 'title': room.find('a').text} for room in room_elements]
        content['rooms'] = rooms

        code = re.search(r'\(([A-Z4]*)\)?$', content['title']).group(1)

        data[code] = content
    
    with open(CACHED_FILE_PATH, 'w') as outfile:
        json.dump(data, outfile)
    
    return data


def get() -> dict:
    """
    Gets the room urls data either from cache or online
    """
    if os.path.isfile(CACHED_FILE_PATH):
        with open(CACHED_FILE_PATH) as f:
            data = json.load(f)
        return data
    else:
        return cache()

if __name__ == '__main__':
    urls = get()
    print(urls)

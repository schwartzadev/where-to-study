import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.colorado.edu/students/find-your-study-spot')
soup = BeautifulSoup(response.content)

all_cards = soup.find_all('div', {'class': 'content-grid-item-inner'})

building_cards = [
    card for card in all_cards if card.find('h2', {'class': 'feature-callout-title'}) is not None
]

data = []

for building in building_cards:
    content = {}
    content['title'] = building.find('h2', {'class': 'feature-callout-title'}).text
    room_elements = building.find_all('li')
    rooms = [{'destination': room.find('a')['href'].split('?ce/')[0], 'title': room.find('a').text} for room in room_elements]

    content['rooms'] = rooms

    data.append(content)

print(data)
import pdb
pdb.set_trace()

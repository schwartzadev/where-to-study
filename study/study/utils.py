import json
from pathlib import Path
from datetime import date
import requests
import json

"""
Utilities to get available rooms
"""


def get_building_density(day_of_week: str) -> dict:
    path = Path('building_data/density_trends') /  Path(day_of_week.lower() + '.json')
    with open(path) as f:
        data = json.load(f)
    return data

def get_room_availability_data() -> dict:
    """Gets and parses availability data from ems.colorado.edu

    Returns:
        dict: A cleaned array of building data
    """
    # todo remove the headers that aren't required
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://ems.colorado.edu',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://ems.colorado.edu/BrowseForSpace.aspx',
        'TE': 'Trailers',
    }

    # todo set dates in here

    post_data = '{"filterData":{"filters":[{"filterName":"StartDate","value":"2021-03-6 12:00:00","displayValue":null,"filterType":3},{"filterName":"EndDate","value":"2021-03-7 12:00:00","filterType":3,"displayValue":""},{"filterName":"Locations","value":"-1","displayValue":"(all)","filterType":8},{"filterName":"TimeZone","value":"68","displayValue":"","filterType":2},{"filterName":"RoomTypes","value":"120","displayValue":"Study","filterType":7}]}}'

    response = requests.post('https://ems.colorado.edu/ServerApi.aspx/GetBrowseLocationsRooms',
        headers=headers,
        data=post_data,
    )

    data = json.loads(response.content)

    d = json.loads(data['d'])
    raw_buildings_data = d['Buildings']

    clean_buildings = []
    for building in raw_buildings_data:
        rooms = [room['Description'] for room in building['Rooms']]
        
        # Don't add the building if it has no rooms.
        if len(rooms) > 0:
            clean_buildings.append({
                "code": building['Code'].replace('B_', ''),
                "label": building['DisplayText'],
                "rooms": rooms
            })

    return clean_buildings


def get_current_building_density() -> dict:
    today_weekday = date.today().strftime('%A')
    return get_building_density(today_weekday)


def get_available_rooms():
    """
    Combines density data and available room data.
    """
    available_buildings =  get_room_availability_data()
    current_density = get_current_building_density()

    density_dict = {}

    for building in current_density:
        density_dict[building["buildingCode"]] = building

    for building in available_buildings:
        code = building['code']
        try:
            density_info = density_dict[code]
            building['density'] = density_info['trendData']
        except KeyError as e:
            # Building does not exist in the density data...
            building['density'] = None

    return available_buildings
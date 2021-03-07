import json
from pathlib import Path
from datetime import date, datetime, timedelta
import requests
import json
import pytz

from study import room_urls

"""
Utilities to get available rooms
"""

def _get_ems_post_data() -> str:
    today = date.today()
    today_string = today.strftime('%Y-%m-%-d')

    tomorrow_string = (today + timedelta(days=1)).strftime('%Y-%m-%-d')

    data = '{{"filterData":{{"filters":[{{"filterName":"StartDate","value":"{today} 12:00:00","displayValue":null,"filterType":3}},{{"filterName":"EndDate","value":"{tomorrow} 12:00:00","filterType":3,"displayValue":""}},{{"filterName":"Locations","value":"-1","displayValue":"(all)","filterType":8}},{{"filterName":"TimeZone","value":"68","displayValue":"","filterType":2}},{{"filterName":"RoomTypes","value":"120","displayValue":"Study","filterType":7}}]}}}}'.format(today=today_string, tomorrow=tomorrow_string)

    return data

def get_building_density(day_of_week: str) -> dict:
    path = Path('building_data/density_trends') /  Path(day_of_week.lower() + '.json')
    with open(path) as f:
        data = json.load(f)
    return data

def get_building_info() -> dict:
    path = Path('building_data/building_info.json')
    with open(path) as f:
        building_info = json.load(f)
    
    building_dict = {}
    for building in building_info:
        code = building['code']
        building_dict[code] = building
    return building_dict


def get_building_availability_data() -> dict:
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

    post_data = _get_ems_post_data()

    response = requests.post('https://ems.colorado.edu/ServerApi.aspx/GetBrowseLocationsRooms',
        headers=headers,
        data=post_data,
    )

    data = json.loads(response.content)

    d = json.loads(data['d'])
    raw_buildings_data = d['Buildings']

    clean_buildings = []
    for building in raw_buildings_data:
        rooms = [{ "name": room['Description'], "id": room['Id']} for room in building['Rooms']]
        
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


def filter_rooms_by_bookings(original_rooms: list) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json; charset=utf-8',
        'dea-CSRFToken': 'cbb94c0b-118b-471e-9a07-aba59b53a5b3',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://ems.colorado.edu',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://ems.colorado.edu/BrowseForSpace.aspx',
        'TE': 'Trailers',
    }

    data = _get_ems_post_data()

    response = requests.post('https://ems.colorado.edu/ServerApi.aspx/GetBrowseLocationsBookings', headers=headers, data=data)

    data = json.loads(response.content)

    d = data['d']

    bookings = json.loads(d)['Bookings']

    # This filters out any room that has a booking in the current time period.
    # This does *not* filter out rooms based on the time of the booking.

    booked_rooms = [room['BookingInRoomId'] for room in bookings]

    available_rooms = [room for room in original_rooms if room['id'] not in booked_rooms]

    return available_rooms


def get_available_rooms():
    """
    Combines density data and available room data.
    """
    available_buildings =  get_building_availability_data()
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
    
    rooms = []
    
    tz = pytz.timezone('US/Mountain')

    current_hour = datetime.now(tz).strftime('%-H')

    for building in available_buildings:
        if building['density'] is None:
            # Don't add to rooms
            continue
        current_density = [hour for hour in building['density'] if hour['hourOfDay'] is int(current_hour)]
        if current_density is not None:
            current_density = current_density[0]['density']
        for room in building['rooms']:
            rooms.append({
                "label": room['name'],
                "id": room['id'],
                "building_code": building["code"],
                "building_label": building["label"],
                "density": current_density
            })

    filtered_rooms = filter_rooms_by_bookings(rooms)

    # Add address data
    building_info = get_building_info()
    urls = room_urls.get()

    rooms_with_urls = []

    for room in filtered_rooms:
        code = room['building_code']
        try:
            building_url_info = urls[code]
            room['address'] = building_info[code]['address']
            room['map_hash'] = room_urls.match_string_to_room(
                room['label'],
                building_url_info['rooms'],
            )
            rooms_with_urls.append(room)
        except KeyError:
            # Skip rooms that aren't in buildings with associated URLs.
            pass

    return rooms_with_urls

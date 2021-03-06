import json
from pathlib import Path
from datetime import date

"""
Utilities to get available rooms
"""


def get_building_density(day_of_week: str) -> dict:
    path = Path('building_data/density_trends') /  Path(day_of_week.lower() + '.json')
    with open(path) as f:
        data = json.load(f)
    return data


def get_current_building_density() -> dict:
    today_weekday = date.today().strftime('%A')
    return get_building_density(today_weekday)

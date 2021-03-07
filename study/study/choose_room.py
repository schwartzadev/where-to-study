import random
import json

from study import utils

def _get_weights(rooms) -> list:
    weights = [( 1 - room['density']) for room in rooms]
    return weights


def _choose_from_list(rooms: list) -> dict:
    return random.choices(rooms, weights=_get_weights(rooms))[0]


def choose_random() -> dict:
    """
    Randomly chooses a room based on the inverse of its density
    """
    rooms = utils.get_available_rooms()

    return _choose_from_list(rooms)


def choose_from_cache() -> dict:
    """
    Randomly chooses a room from the cache.
    """
    with open('rooms_cache.json') as file:
        data = json.load(file)
    
    rooms = data['rooms']

    room = _choose_from_list(rooms)

    return room
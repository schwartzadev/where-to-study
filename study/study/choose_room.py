from study import utils
import random

def _get_weights(rooms) -> list:
    weights = [( 1 - room['density']) for room in rooms]
    return weights


def choose_random() -> dict:
    """
    Randomly chooses a room based on the inverse of its density
    """
    rooms = utils.get_available_rooms()

    room = random.choices(rooms, weights=_get_weights(rooms))[0]

    return room

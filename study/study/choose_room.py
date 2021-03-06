from study import utils
import random

def choose_random() -> dict:
    """
    Randomly chooses a room based on the inverse of its density
    """
    rooms = utils.get_available_rooms()
    
    weights = [( 1 - room['density']) for room in rooms]

    room = random.choices(rooms, weights=weights)

    return room

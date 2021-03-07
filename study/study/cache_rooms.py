import json
from datetime import datetime

from study import utils
from study import choose_room

def cache():
    rooms = utils.get_available_rooms()

    to_save = {
        'updated': datetime.now().timestamp(),
        'rooms': rooms
    }

    with open('rooms_cache.json', 'w') as outfile:
        json.dump(to_save, outfile)

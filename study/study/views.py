import json
import pprint

from django.http import JsonResponse

from study import utils

def index(request):
    data = utils.get_current_building_density()
    available = utils.get_available_rooms() # debugging
    return JsonResponse(available, safe=False)

from django.http import HttpResponse

from study import utils

def index(request):
    data = utils.get_current_building_density()
    utils.get_available_rooms() # debugging
    return HttpResponse(data)

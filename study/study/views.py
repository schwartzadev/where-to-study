from django.http import HttpResponse

from study import utils

def index(request):
    data = utils.get_current_building_density()
    return HttpResponse(utils.get_current_building_density())

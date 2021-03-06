from django.http import JsonResponse
from django.views.generic.base import TemplateView

from study import choose_room

def index(request):
    room = choose_room.choose_random() # debugging
    return JsonResponse(room, safe=False)

class MapView(TemplateView):
    template_name = "map.html"

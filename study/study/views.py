from django.http import JsonResponse
from django.views.generic.base import TemplateView

from study import choose_room

class MapView(TemplateView):
    template_name = "map.html"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['room'] = choose_room.choose_from_cache()
        return data

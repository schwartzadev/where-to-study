from django.http import JsonResponse
from django.views.generic.base import TemplateView
import after_response

from study import choose_room
from study import cache_rooms

class MapView(TemplateView):
    template_name = "map.html"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['room'] = choose_room.choose_from_cache()
    
        @after_response.enable
        def update_cache():
            cache_rooms.cache()

        # Updates the cache after each response.
        update_cache.after_response()

        return data

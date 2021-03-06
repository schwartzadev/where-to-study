from django.http import JsonResponse

from study import choose_room

def index(request):
    room = choose_room.choose_random() # debugging
    return JsonResponse(room, safe=False)

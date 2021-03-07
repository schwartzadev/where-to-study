from django.contrib import admin
from django.urls import path

from study import views

from study import cache_rooms

# Runs once on startup
cache_rooms.cache()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('map', views.MapView.as_view(), name='map'),
    path('map/', views.MapView.as_view(), name='map'),
    path('', views.IndexView.as_view(), name='index'),
]

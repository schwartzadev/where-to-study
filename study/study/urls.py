from django.contrib import admin
from django.urls import path

from study import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('map', views.MapView.as_view(), name='map'),
    path('map/', views.MapView.as_view(), name='map'),
    path('', views.IndexView.as_view(), name='index'),
]

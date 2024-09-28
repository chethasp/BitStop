from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('getlocations/', views.locations)
    path('get_lat_long/', get_lat_long_view, name='get_lat_long'),
]

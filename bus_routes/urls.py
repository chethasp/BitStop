from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('get_lat_long/', views.get_lat_long_view, name='get_lat_long'),  # Accessing the get_lat_long_view
    path('generate_foot_traffic_sites/', views.get_foot_traffic_data, name='generate_foot_traffic_sites')
]

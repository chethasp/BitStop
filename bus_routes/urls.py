from django.urls import path 
from . import views 

#URLConf

urlpattern = [
    path('getlocations/', views.locations)
]
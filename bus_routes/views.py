from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse

from bus_routes import Node

# Create your views here.

def locations(request):
    coordinates = Node.get_coordinates()

    # Return the list of coordinates as a JSON response
    return JsonResponse({'coordinates': coordinates})
     
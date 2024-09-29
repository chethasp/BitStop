from django.shortcuts import render
from django.http import JsonResponse

from bus_routes.googlecoords import get_lat_long
from bus_routes.foot_traffic_sites import get_sites
from bus_routes.graph_operations import get_routes

from django.views.decorators.http import require_GET

# Create your views here.

@require_GET
def get_lat_long_view(request):
    address = request.GET.get('address')  # Get the address from query parameters
    if not address:
        return JsonResponse({'error': 'No address provided'}, status=400)
    
    lat_lng = get_lat_long(address)
    if lat_lng:
        lat, lng = lat_lng
        return JsonResponse({'latitude': lat, 'longitude': lng})
    else:
        return JsonResponse({'error': 'Could not retrieve coordinates.'}, status=500)
    
def get_foot_traffic_data(request):
    city = request.GET.get('city')
    amount = request.GET.get('amount')
    get_sites(city, amount)
    get_routes()
    return JsonResponse({'routes generated?': 'true'})
from django.shortcuts import render
from django.http import JsonResponse

from bus_routes.googlecoords import get_lat_long

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
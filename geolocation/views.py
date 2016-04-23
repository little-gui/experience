from geopy.geocoders import GoogleV3
from ipware.ip import get_ip

from geolocation.models import Location
from utils.decorators import render_to


@render_to('geolocation.html')
def index(request):
    """ receives latitude, longitude or address and save on database """
    if request.method == 'POST':
        address = request.POST.get('address')

        # address gets priority if its filled
        if address:
            # get latitude and longitude from google api with provided address
            googlev3 = GoogleV3()
            location = googlev3.geocode(address)
            longitude = location.longitude
            latitude = location.latitude
        else:
            # get longitude and latitude the browser might provided
            latitude = request.POST.get('latitude') 
            longitude = request.POST.get('longitude')

        if latitude != '':
            # get ip from request and save with geolocation
            request_ip = get_ip(request)
            Location.objects.update_or_create(ip=request_ip, defaults={
                "longitude": longitude, "latitude": latitude})

    return {"locations": Location.objects.all()}


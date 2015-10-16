from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

__author__ = 'marcio'


class GeoSearch:
    def __init__(self):
        self.geolocator = Nominatim()

    def search(self, address):
        try:
            location = self.geolocator.geocode(address, timeout=20)
            if location:
                lat = location.latitude
                long = location.longitude
                full_address = location.address
                if 40.485808 < lat < 40.917691 and -73.699206 > long > -74.260380:
                    return lat, long, full_address
                else:
                    return None, None
            else:
                return None, None
        except (GeocoderTimedOut, AttributeError):
            return None, None

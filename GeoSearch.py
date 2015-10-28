from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.geocoders import OpenMapQuest
from omgeo import Geocoder
from Normalizer import Normalizer

__author__ = 'marcio'


class GeoSearch:
    def __init__(self, dao=None):
        self.geolocator_n = Nominatim()
        self.geolocator_omq = OpenMapQuest()
        self.dao = dao
        self.g = Geocoder()

    def search_nominatim(self, address):
        try:
            location = self.geolocator_n.geocode(address, timeout=20)
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

    def search_openmapquest(self, address):
        try:
            location = self.geolocator_omq.geocode(address, timeout=20)
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

    def search_dao(self, address, borough):
        results = self.dao.do("SELECT ST_X(geomout), ST_Y(geomout), "
                              "(addy).zip FROM geocode('" + address + "') As g;")
        return self.verify_address(results, borough)

    @staticmethod
    def verify_address(results, borough):
        zips = Normalizer.select_zipcode_class(borough)
        for r in results:
            zip3dig = int(r[2]) / 100
            if zip3dig in zips:
                return r[0], r[1]
        return None

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.geocoders import OpenCage
from geopy.geocoders import Bing
from Normalizer import Normalizer
from random import randint

__author__ = 'marcio'


class GeoSearch:
    def __init__(self, dao=None):
        self.geolocator_nominatim = None
        self.geolocator_google = None
        self.geolocator_opencage = None
        self.geolocator_bing = None
        self.dao = dao

    def search_nominatim(self, address):
        try:
            self.geolocator_nominatim = Nominatim(proxies={'http': self.get_proxy()})
            location = self.geolocator_nominatim.geocode(address, timeout=20)
            if location:
                lat = location.latitude
                lon = location.longitude
                full_address = location.address
                if 40.485808 < lat < 40.917691 and -73.699206 > lon > -74.260380:
                    return lat, lon, full_address
                else:
                    return None, None
            else:
                return None, None
        except (GeocoderTimedOut, AttributeError):
            return None, None

    def search_google(self, address):
        try:
            self.geolocator_google = GoogleV3(api_key='AIzaSyAwv1G4XIza'
                                              '5IIlwucRjWZlFA3lbynGG_8',
                                              proxies={'http': self.get_proxy()})
            location = self.geolocator_google.geocode(address, timeout=20)
            if location:
                lat = location.latitude
                lon = location.longitude
                full_address = location.address
                if 40.485808 < lat < 40.917691 and -73.699206 > lon > -74.260380:
                    return lat, lon, full_address
                else:
                    return None, None
            else:
                return None, None
        except (GeocoderTimedOut, AttributeError):
            return None, None

    def search_opencage(self, address):
        try:
            self.geolocator_opencage = OpenCage(api_key='d65ff98d8e33b1b85210ed4a400fc3a1',
                                                proxies={'http': self.get_proxy()})
            location = self.geolocator_opencage.geocode(address, timeout=20)
            if location:
                lat = location.latitude
                lon = location.longitude
                full_address = location.address
                if 40.485808 < lat < 40.917691 and -73.699206 > lon > -74.260380:
                    return lat, lon, full_address
                else:
                    return None, None
            else:
                return None, None
        except (GeocoderTimedOut, AttributeError):
            return None, None

    def search_bing(self, address):
        try:
            self.geolocator_bing = Bing(api_key='AuqD7e7LRzuD5Wzmn2HqTQPIipUyZrbgz2y_'
                                        'efTS9YtGhio37GkJr9IWmnRV4EOB',
                                        proxies={'http': self.get_proxy()})
            location = self.geolocator_bing.geocode(address, timeout=20)
            if location:
                lat = location.latitude
                lon = location.longitude
                full_address = location.address
                if 40.485808 < lat < 40.917691 and -73.699206 > lon > -74.260380:
                    return lat, lon, full_address
                else:
                    return None, None
            else:
                return None, None
        except (GeocoderTimedOut, AttributeError):
            return None, None

    def search_dao(self, address, borough):
        results = self.dao.do("SELECT ST_X(geomout), ST_Y(geomout), "
                              "(addy).zip FROM geocode('" + address + "') As g LIMIT 1;")
        return self.verify_address(address, results, borough)

    @staticmethod
    def verify_address(adress, results, borough):
        zips = Normalizer.select_zipcode_class(borough)
        for r in results:
            zip3dig = int(r[2]) / 100
            if zip3dig in zips:
                return r[0], r[1], adress+", "+r[2]
        return None

    def get_proxy(self):
        proxies = ['durianproxy.gq', 'proxyrocket.org', 'apricotproxy.gq',
                   'technoproxy.cf', 'mawoop.ml', 'proxyfree.party', 'accessproxy.org',
                   'proxyeuro.pw', 'zqal.xyz', 'bukus.ga', 'popeyeprox.info', 'b2bproxy.cf',
                   'buzy.ml', 'limeproxy.gq', 'web.proxygogo.info', 'broccoliproxy.gq',
                   'xyzproxy.gq', 'franceproxy.pw', 'ispvpn.com'
                   ]
        return proxies[randint(0, len(proxies) - 1)]

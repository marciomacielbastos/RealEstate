from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from GeoSearch import GeoSearch
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'


class BingGeocode:
    def __init__(self, progress, error_log, geo):
        self.error_log = error_log
        self.progress = progress
        self.geo = geo

    def get_coordinates(self, t):
        try:
            bbl = t[0]
            address = Normalizer.set_address(t[1], bbl)
            lat, lon, full_address = self.geo.search_nominatim(address)
            print lat, lon, full_address
            if lat is None:
                raise ValueError
            num = RealEstateSettings.read_progress()+1
            RealEstateSettings.write_progress(num)
            return (bbl, t[1], full_address, long, lat, 1), num
        except ValueError:
            self.error_log.open()
            self.error_log.write(t[1]+", "+str(t[0]))
            self.error_log.close()
            return "Lat, Long not found", -1
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()
            return e.message, -2
        except KeyboardInterrupt:
            return "Stopped", -3

    @staticmethod
    def get_num():
        return 4

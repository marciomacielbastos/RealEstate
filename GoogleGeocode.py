from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
import time
from CsvManager import CsvManager
from Normalizer import Normalizer

__author__ = 'marcio'


class GoogleGeocode:
    def __init__(self, progress, error_log, geo):
        self.error_log = error_log
        self.progress = progress
        self.geo = geo

    def get_coordinates(self, t):
        try:
            bbl = t[0]
            address = Normalizer.set_address(t[1], bbl)
            lat, lon, full_address = self.geo.search_nominatim(address)
            if lat is None:
                raise ValueError
            GoogleGeocode.print_status(" Google")
            num = CsvManager.read_progress()+1
            CsvManager.write_progress(num)
            return (bbl, t[1], full_address, lon, lat, 1), num
        except ValueError:
            self.error_log.open()
            self.error_log.write(t[1]+", "+str(t[0]))
            self.error_log.close()
            GoogleGeocode.print_status(" Lat, Long not found ")
            return -1, False
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()
            GoogleGeocode.print_status(e.message)
            return -2, False
        except KeyboardInterrupt:
            GoogleGeocode.print_status(" Stopped ")
            return -3, False

    @staticmethod
    def get_num():
        return 2

    @staticmethod
    def print_status(string):
        sys.stdout.flush()
        sys.stdout.write(string)
        time.sleep(1)
        sys.stdout.flush()
